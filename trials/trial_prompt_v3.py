"""Deneme 12: düzeltilmiş soru (v3) yeni sitelerde, eski soruyla (v2) yan yana.

Kullanım: trial_prompt_v3.py fetch   -> 15 yeni siteyi okur, kaydeder, etiketleme için özet basar
          trial_prompt_v3.py run     -> kayıtlı metinleri iki soruyla Groq'a sorar
Kriter (denemeden önce yazıldı):
- v3'te kanıt cümlelerinin en az %95'i gönderilen metinde geçmeli (parçalı kontrolle).
- v3'te "kendi yazılımını geliştiriyor mu" etiketli sitelerin en az %85'inde doğru olmalı ve v2'den düşük olmamalı.
- Okunamayan siteye "unknown" denmeli.
"""
import json
import random
import re
import sys

from playwright.sync_api import sync_playwright

from sitefind import OUT, ca_bundle, host, load_companies, lower_tr
from sitescan import build_document, lines, scan_site
from trial_site_scan import SEEN

TRIAL9 = {"t2.com.tr", "bncool.com.tr", "oska.com.tr", "zeo.org", "a2labs.com.tr", "antenom.com", "innocentrum.com", "pleksus.com.tr",
          "umram.bilkent.edu.tr", "tomboprint.com", "moralabs.com", "keyyazilim.com", "konumsal.com.tr", "egyazilim.com", "birfatura.com"}
DOCS = OUT / "prompt_v3_docs"
AI_RX = re.compile(r"yapay zeka|artificial intelligence|makine ogren|machine learning|\bai\b|\bgpt\b|\bllm\b|derin ogren|deep learning")


def sample() -> list[tuple[str, str, str]]:
    pool = [c for c in load_companies() if c[1] and host(c[1]) and host(c[1]) not in SEEN | TRIAL9]
    random.seed(20261125)
    return random.sample(pool, 15)


def fetch() -> None:
    bundle = ca_bundle()
    DOCS.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for name, url, sector in sample():
            pages = scan_site(url, bundle, browser)
            document = build_document(pages) if pages else ""
            (DOCS / f"{host(url)}.txt").write_text(document, encoding="utf-8")
            print(f"\n=== {host(url)}  [{name[:45]}]  sektör: {sector[:40] or '-'}")
            print(f"  sayfalar: {[(c, u[-45:]) for c, u, _ in pages]}  kelime={len(document.split())}")
            body = [l for l in document.split("\n") if len(l.split()) >= 9 and not l.startswith("###")]
            for l in body[:4]:
                print("   ", l[:230])
            ai = [l for l in document.split("\n") if AI_RX.search(lower_tr(l))]
            for l in ai[:3]:
                print("    AI:", l[:200])
        browser.close()


Y, N, NU = ["yes"], ["no"], ["no", "unknown"]
# Groq çalıştırılmadan önce elle yazıldı (2026-11-14). (own_software, ai_in_product). None: etiket kesin değil, sayılmaz.
LABELS = {
    "adim.tech": (N, None), "figensoft.com": (Y, NU), "kv331audio.com": (Y, NU), "netcad.com": (Y, None), "ekinokssoftware.com": (Y, Y),
    "appsamurai.com": (None, NU), "mobileaction.co": (Y, Y), "iliksoft.com": (Y, Y), "codebase.com.tr": (Y, NU), "roketsan.com.tr": (N, NU),
    "mapyazilim.com": (Y, NU), "teknikgrup.com": (N, NU), "bilten.com.tr": (N, NU), "fabric-ate.com": (None, NU), "pointo.com.tr": (Y, None),
}


def run() -> None:
    from groq_extract import SYSTEM, SYSTEM_V3, extract
    from sitefind import read_key

    api_key = read_key("GROQ_API_KEY")
    out_file = OUT / "trial_prompt_v3.json"
    # Yarıda kalan çalışma kaldığı yerden devam eder: hatasız biten (site, soru) çiftleri tekrar sorulmaz.
    results = json.loads(out_file.read_text(encoding="utf-8")) if out_file.exists() else {}
    for site, (own_label, ai_label) in LABELS.items():
        document = (DOCS / f"{site}.txt").read_text(encoding="utf-8")
        results.setdefault(site, {})
        for label, system in (("v2", SYSTEM), ("v3", SYSTEM_V3)):
            if label in results[site] and not results[site][label]["error"]:
                continue
            res = extract(document, api_key, system)
            if (res["error"] or "").startswith("daily_limit"):
                print(f"GÜNLÜK SINIR: {res['error']}\nDurduruldu. Sınır açılınca aynı komut kaldığı yerden devam eder.", flush=True)
                return
            out = res["output"] or {}
            own = (out.get("own_software") or {}).get("value")
            ai = (out.get("ai_in_product") or {}).get("value")
            results[site][label] = {**res, "own_ok": None if own_label is None else own in own_label, "ai_ok": None if ai_label is None else ai in ai_label}
            q = res["quotes"]
            print(f"{site:20} {label} own={own} ({(out.get('own_software') or {}).get('kind')}) {'' if own_label is None else ('OK' if own in own_label else 'FARKLI')} | "
                  f"ai={ai} ({(out.get('ai_in_product') or {}).get('product')}) {'' if ai_label is None else ('OK' if ai in ai_label else 'FARKLI')} | "
                  f"kanıt={[q.get(f) for f in ('what', 'own_software', 'ai_in_product')]} {res['error'] or ''}", flush=True)
            print(f"{'':23} what: {(out.get('what') or {}).get('value')}", flush=True)
            print(f"{'':23} own kanıt: {(out.get('own_software') or {}).get('quote')}", flush=True)
            if ai == "yes":
                print(f"{'':23} ai kanıt: {(out.get('ai_in_product') or {}).get('quote')}", flush=True)
            out_file.write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nÖZET")
    for label in ("v2", "v3"):
        rows = [results[s][label] for s in results if label in results[s] and not results[s][label]["error"]]
        own = [r["own_ok"] for r in rows if r["own_ok"] is not None]
        ai = [r["ai_ok"] for r in rows if r["ai_ok"] is not None]
        quotes = [q for r in rows for q in r["quotes"].values() if q]
        print(f"  {label} own_software {sum(own)}/{len(own)} | ai {sum(ai)}/{len(ai)} | kanıt: aynen={quotes.count('found')} parçalı={quotes.count('found_parts')} "
              f"yok={quotes.count('missing')} toplam={len(quotes)} | hata {sum(1 for r in rows if r['error'])}", flush=True)
    print("BİTTİ", flush=True)


if __name__ == "__main__":
    if sys.argv[1:] == ["fetch"]:
        fetch()
    elif sys.argv[1:] == ["run"]:
        run()
    else:
        raise SystemExit("kullanım: trial_prompt_v3.py fetch | run")
