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

# Deneme 12'de sınanan düzeltilmiş soru (FINDINGS bölüm 19'daki iki soruna karşı):
# kanıtta kelime sınırı yok ve kısaltma yasak; "danışmanlık" hayır örneklerinden çıktı; müşteriye yazılım geliştirmek açıkça yes.
SYSTEM_V3 = """Bir şirketin web sitesinden alınmış sayfa metinlerini okuyacaksın. Sadece bu metinlere dayan; şirket hakkında başka bildiğin hiçbir şeyi kullanma. Şirketin adı tek başına kanıt değildir.
Şu JSON'u döndür:
{"what": {"value": "şirketin ne iş yaptığı, tek cümle, Türkçe", "quote": "..."},
 "own_software": {"value": "yes | no | unknown", "kind": "yazılımın türü, kısa (ör. web platformu, mobil uygulama, gömülü yazılım, müşteriye özel yazılım) ya da boş", "quote": "..."},
 "ai_in_product": {"value": "yes | no | unknown", "product": "ürün adı ya da boş", "quote": "..."}}
Tanımlar:
- own_software yes: şirketin çalışanları yazılım geliştiriyor. Üç durum da yes: (1) kendi yazılım ürünü, platformu ya da uygulaması var; (2) müşteriler için özel yazılım geliştiriyor; (3) yazılımın yanında başka iş de yapıyor (danışmanlık, donanım, eğitim) ama yazılım da geliştiriyor.
- own_software no: metin şirketin işini anlatıyor ve bu işin içinde yazılım geliştirmek yok (ör. laboratuvar, üretim, donanım ya da çip tasarımı, mühendislik hizmeti, pazarlama, etkinlik). Başkasının ürününü satmak, dağıtmak ya da kurmak tek başına yes değildir.
- own_software unknown: metin şirketin ne iş yaptığını anlatmıyor ya da karar verecek kadar bilgi yok.
- what alanına şirketin yazılım geliştirdiğini yazdıysan own_software yes olmalı; ikisi çelişmemeli.
- ai_in_product yes: adı geçen somut bir üründe yapay zekânın ne yaptığı anlatılıyor. Genel slogan ya da genel hizmet başlığı yes sayılmaz. Metin şirketin ürünlerini anlatmıyorsa unknown.
Kurallar:
- quote, metindeki TEK bir cümlenin ya da satırın HARFİ HARFİNE kopyası olmalı. Kelime sınırı yok. Cümleyi kısaltma, "..." kullanma, iki ayrı yeri birleştirme, çevirme, düzeltme. Cümle çok uzunsa kesintisiz bir parçasını al.
- Menüdeki isim listesi kanıt değildir.
- value "yes" ya da "no" ise (ai_in_product "no" hariç) quote zorunlu. Kanıt yoksa value "unknown", quote "" olsun. Tahmin yürütme."""

FIELDS = ("what", "own_software", "ai_in_product")
_INVISIBLE = re.compile("[​‌‍﻿­⁠]")
_DASH = re.compile("[‐‑‒–—−]")


def normalize(text: str) -> str:
    """Kanıt kontrolünde yok sayılan farklar: tire türü, görünmez karakter, boşluk, büyük-küçük harf."""
    return " ".join(_DASH.sub("-", _INVISIBLE.sub("", text)).split()).casefold()


_ELLIPSIS = re.compile(r"\.{3,}|…")


def quote_status(quote: str, document_normalized: str) -> str | None:
    """None: kanıt yok. found: metinde aynen geçiyor. found_parts: "..." ile kısaltılmış ama parçaların hepsi
    metinde sırayla geçiyor. missing: geçmiyor."""
    q = normalize(quote)
    if not q:
        return None
    if q in document_normalized:
        return "found"
    parts = [normalize(part) for part in _ELLIPSIS.split(quote)]
    parts = [part for part in parts if len(part.split()) >= 2]
    if len(parts) < 2:
        return "missing"
    position = 0
    for part in parts:
        index = document_normalized.find(part, position)
        if index < 0:
            return "missing"
        position = index + len(part)
    return "found_parts"


def check_quotes(output: dict, document: str) -> dict[str, str | None]:
    """Her alanın kanıt cümlesi gönderilen metinde geçiyor mu."""
    doc = normalize(document)
    return {field: quote_status((output.get(field) or {}).get("quote") or "", doc) for field in FIELDS}


def _seconds(value: str) -> float:
    """'1m26.4s' ya da '46.672s' -> saniye."""
    m = re.fullmatch(r"(?:(\d+)m)?([\d.]+)s", value or "")
    return (int(m.group(1) or 0) * 60 + float(m.group(2))) if m else 60.0


def extract(document: str, api_key: str, system: str = SYSTEM) -> dict:
    """Metni Groq'a sorar. Dakikalık token sınırına takılırsa bekleyip tekrar dener.

    Döner: {"output": dict | None, "quotes": dict, "usage": dict, "error": str | None}
    """
    body = {"model": MODEL, "temperature": 0, "response_format": {"type": "json_object"}, "reasoning_effort": "low",
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": document}]}
    for _attempt in range(8):
        r = requests.post("https://api.groq.com/openai/v1/chat/completions", headers={"Authorization": f"Bearer {api_key}"}, json=body, timeout=180)
        if r.status_code == 429:
            # Günlük token sınırı (TPD) dolduysa beklemek dakikalar ya da saatler sürer: bekleme, hemen bildir.
            if "tokens per day" in r.text:
                return {"output": None, "quotes": {}, "usage": {}, "error": f"daily_limit: {r.json()['error']['message'][:160]}"}
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
