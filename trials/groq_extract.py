"""Groq ile siteden olgu çıkarma: soru metni, çağrı ve kanıt kontrolü."""
import json
import re
import time

import requests

MODEL = "openai/gpt-oss-120b"

# FINDINGS bölüm 4'te (deneme 2) kullanılan soru metni. Değiştirilirse yeni bir deneme sayılır.
SYSTEM = """Bir şirketin web sitesinden alınmış sayfa metinlerini okuyacaksın. Sadece bu metinlere dayan; şirket hakkında başka bildiğin hiçbir şeyi kullanma. Şirketin adı tek başına kanıt değildir.
Şu JSON'u döndür:
{"what": {"value": "şirketin ne iş yaptığı, tek cümle, Türkçe", "quote": "..."},
 "own_software": {"value": "yes | no | unknown", "kind": "yazılımın türü, kısa (ör. web platformu, mobil uygulama, gömülü yazılım) ya da boş", "quote": "..."},
 "ai_in_product": {"value": "yes | no | unknown", "product": "ürün adı ya da boş", "quote": "..."}}
Tanımlar:
- own_software yes: şirket KENDİSİ yazılım geliştiriyor (kendi yazılım ürünü, platformu, uygulaması ya da müşteriye özel yazılım geliştirme hizmeti).
- own_software no: metin şirketin işini anlatıyor ve bu iş yazılım geliştirmek değil (ör. laboratuvar, donanım ya da çip tasarımı, mühendislik hizmeti, danışmanlık). Başkasının yazılımını ya da ürününü SATMAK, dağıtmak, kurmak yazılım geliştirmek sayılmaz.
- own_software unknown: metin şirketin ne iş yaptığını anlatmıyor ya da karar verecek kadar bilgi yok.
- ai_in_product yes: adı geçen somut bir üründe yapay zekânın ne yaptığı anlatılıyor. Genel slogan yes sayılmaz. Metin şirketin ürünlerini anlatmıyorsa unknown.
Kurallar:
- quote, metinden HARFİ HARFİNE kopyalanmış, en fazla 25 kelimelik kesintisiz bir parça olmalı. Çevirme, düzeltme, kısaltma, birleştirme yapma. Menüdeki isim listesi kanıt değildir.
- value "yes" ya da "no" ise (ai_in_product "no" hariç) quote zorunlu. Kanıt yoksa value "unknown", quote "" olsun. Tahmin yürütme."""

FIELDS = ("what", "own_software", "ai_in_product")
_INVISIBLE = re.compile("[​‌‍﻿­⁠]")
_DASH = re.compile("[‐‑‒–—−]")


def normalize(text: str) -> str:
    """Kanıt kontrolünde yok sayılan farklar: tire türü, görünmez karakter, boşluk, büyük-küçük harf."""
    return " ".join(_DASH.sub("-", _INVISIBLE.sub("", text)).split()).casefold()


def check_quotes(output: dict, document: str) -> dict[str, str | None]:
    """Her alanın kanıt cümlesi gönderilen metinde geçiyor mu. None: kanıt verilmemiş."""
    doc = normalize(document)
    result = {}
    for field in FIELDS:
        quote = normalize((output.get(field) or {}).get("quote") or "")
        result[field] = None if not quote else ("found" if quote in doc else "missing")
    return result


def _seconds(value: str) -> float:
    """'1m26.4s' ya da '46.672s' -> saniye."""
    m = re.fullmatch(r"(?:(\d+)m)?([\d.]+)s", value or "")
    return (int(m.group(1) or 0) * 60 + float(m.group(2))) if m else 60.0


def extract(document: str, api_key: str) -> dict:
    """Metni Groq'a sorar. Dakikalık token sınırına takılırsa bekleyip tekrar dener.

    Döner: {"output": dict | None, "quotes": dict, "usage": dict, "error": str | None}
    """
    body = {"model": MODEL, "temperature": 0, "response_format": {"type": "json_object"}, "reasoning_effort": "low",
            "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": document}]}
    for _attempt in range(8):
        r = requests.post("https://api.groq.com/openai/v1/chat/completions", headers={"Authorization": f"Bearer {api_key}"}, json=body, timeout=180)
        if r.status_code == 429:
            time.sleep(float(r.headers.get("retry-after", 60)) + 2)
            continue
        break
    if r.status_code != 200:
        return {"output": None, "quotes": {}, "usage": {}, "error": f"HTTP {r.status_code} {r.text[:200]}"}
    payload = r.json()
    try:
        output = json.loads(payload["choices"][0]["message"]["content"])
    except Exception as e:  # noqa: BLE001
        return {"output": None, "quotes": {}, "usage": payload.get("usage", {}), "error": f"json: {e}"}
    # Kalan dakikalık token azsa, sıfırlanana kadar bekle ki sonraki istek 429 yemesin.
    if int(r.headers.get("x-ratelimit-remaining-tokens", "8000")) < 7500:
        time.sleep(_seconds(r.headers.get("x-ratelimit-reset-tokens", "60s")) + 1)
    return {"output": output, "quotes": check_quotes(output, document), "usage": payload.get("usage", {}), "error": None}
