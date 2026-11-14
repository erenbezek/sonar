"""Deneme 11: metni temizlemek Groq'un cevabını değiştiriyor mu.

Deneme 9-10'daki sitelerin kayıtlı sayfaları üç metinle sorulur: ham, tekrarları atılmış, trafilatura.
Her metin 2.300 kelimede kesilir. Etiketler denemeden önce elle yazıldı.
Kriter (denemeden önce yazıldı):
- Tekrar atma yönteminin doğru cevap sayısı hamınkinden düşük olmamalı.
- Trafilatura'nın kalması için doğru cevap sayısı tekrar atma yönteminden düşük olmamalı.
- Her yöntemde kanıt cümlelerinin hepsi gönderilen metinde geçmeli.
"""
import json

import trafilatura

from groq_extract import extract
from sitefind import OUT, read_key
from sitescan import drop_repeats, lines

WORD_CAP = 2300
Y, N, NU = ["yes"], ["no"], ["no", "unknown"]
# None: etiket kesin değil, sayılmaz.
LABELS = {
    "t2.com.tr": (Y, NU), "bncool.com.tr": (N, NU), "oska.com.tr": (Y, None), "zeo.org": (None, None), "antenom.com": (N, NU),
    "innocentrum.com": (Y, NU), "pleksus.com.tr": (Y, Y), "umram.bilkent.edu.tr": (N, NU), "tomboprint.com": (Y, NU),
    "moralabs.com": (Y, NU), "keyyazilim.com": (Y, Y), "konumsal.com.tr": (Y, NU), "egyazilim.com": (Y, None), "birfatura.com": (Y, NU),
}


def build(pages: list[tuple[str, list[str]]]) -> str:
    """Sayfaları sırayla birleştirir ve toplam kelimeyi sınırlar."""
    parts, budget = [], WORD_CAP
    for category, page_lines in pages:
        text = "\n".join(page_lines)
        tokens = text.split()
        if not tokens or budget <= 0:
            continue
        if len(tokens) > budget:
            text = " ".join(tokens[:budget])
        budget -= min(len(tokens), budget)
        parts.append(f"### SAYFA: {category}\n{text}")
    return "\n\n".join(parts)


def main() -> None:
    api_key = read_key("GROQ_API_KEY")
    results = {}
    out_file = OUT / "trial_groq_text_variants.json"
    for site, (own_label, ai_label) in LABELS.items():
        site_dir = OUT / "pages" / site
        meta = json.loads((site_dir / "pages.json").read_text())
        htmls = [(category, (site_dir / f"{i}_{category}.html").read_text(encoding="utf-8")) for i, (category, _url) in enumerate(meta)]
        raw = [(c, lines(h)) for c, h in htmls]
        deduped = drop_repeats([l for _, l in raw])
        variants = {
            "raw": build(raw),
            "repeats": build([(c, l) for (c, _), l in zip(raw, deduped)]),
            "traf": build([(c, (trafilatura.extract(h) or "").split("\n")) for c, h in htmls]),
        }
        results[site] = {}
        for label, document in variants.items():
            res = extract(document, api_key)
            out = res["output"] or {}
            own = (out.get("own_software") or {}).get("value")
            ai = (out.get("ai_in_product") or {}).get("value")
            results[site][label] = {**res, "sent_words": len(document.split()),
                                    "own_ok": None if own_label is None else own in own_label,
                                    "ai_ok": None if ai_label is None else ai in ai_label}
            quotes = res["quotes"]
            print(f"{site:22} {label:8} kelime={len(document.split()):5d} token={res['usage'].get('prompt_tokens')} | own={own} ({(out.get('own_software') or {}).get('kind')}) "
                  f"{'' if own_label is None else ('OK' if own in own_label else 'FARKLI')} | ai={ai} ({(out.get('ai_in_product') or {}).get('product')}) "
                  f"{'' if ai_label is None else ('OK' if ai in ai_label else 'FARKLI')} | kanıt={[quotes.get(f) for f in ('what', 'own_software', 'ai_in_product')]} {res['error'] or ''}", flush=True)
            print(f"{'':22} {'':8} what: {(out.get('what') or {}).get('value')}", flush=True)
            for field in ("own_software", "ai_in_product"):
                if quotes.get(field) == "missing":
                    print(f"{'':31} KAYIP KANIT [{field}]: {(out.get(field) or {}).get('quote')}", flush=True)
            out_file.write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nÖZET")
    for label in ("raw", "repeats", "traf"):
        rows = [results[s][label] for s in results]
        own = [r["own_ok"] for r in rows if r["own_ok"] is not None]
        ai = [r["ai_ok"] for r in rows if r["ai_ok"] is not None]
        quotes = [q for r in rows for q in r["quotes"].values() if q]
        tokens = sum(r["usage"].get("prompt_tokens", 0) for r in rows)
        print(f"  {label:8} own_software {sum(own)}/{len(own)} | ai {sum(ai)}/{len(ai)} | toplam {sum(own)+sum(ai)}/{len(own)+len(ai)} | "
              f"kanıt {quotes.count('found')}/{len(quotes)} | hata {sum(1 for r in rows if r['error'])} | giriş token {tokens}", flush=True)
    print("BİTTİ", flush=True)


if __name__ == "__main__":
    main()
