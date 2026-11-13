"""Deneme 10: Groq'a gidecek metni temizleme. Ham, trafilatura (iki ayar) ve tekrar eden satırı atma karşılaştırılır.

Ölçü: ham metindeki en az 12 kelimelik satırlar "içerik cümlesi" sayılır.
Kriter (denemeden önce yazıldı), bir yöntemin kullanılabilir sayılması için:
- metin, sitelerin ortancasında en az %30 kısalmalı;
- içerik cümlelerinin ortancada en az %90'ı korunmalı;
- en kötü sitede bile en az %50'si korunmalı.
"""
import json
import random
import statistics

import trafilatura
from playwright.sync_api import sync_playwright

from sitefind import OUT, ca_bundle, host, load_companies
from sitescan import BROWSER_THRESHOLD, drop_repeats, get, lines, parse, read_home, render, select_pages
from trial_site_scan import SEEN

LONG = 12  # bu kadar ya da daha fazla kelimeli satır içerik cümlesi sayılır
norm = lambda s: " ".join(s.split()).casefold()


def main() -> None:
    bundle = ca_bundle()
    pool = [c for c in load_companies() if c[1] and host(c[1]) and host(c[1]) not in SEEN]
    random.seed(20261124)  # deneme 9 ile aynı 15 şirket
    sample = random.sample(pool, 15)
    pages_dir = OUT / "pages"
    rows = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for name, url, _sector in sample:
            final, html, _note = read_home(url, bundle)
            if not html:
                print(f"{host(url):24} açılmadı"); continue
            use_browser = len(parse(html)[0].split()) < BROWSER_THRESHOLD
            if use_browser:
                final, html = render(browser, final)
            htmls = [("home", final, html)]
            picks = select_pages(final, parse(html)[1])
            for category in ("product", "about", "career"):
                for page_url, _text, _score in picks.get(category, []):
                    _, page_html = render(browser, page_url) if use_browser else get(page_url, bundle)
                    if page_html:
                        htmls.append((category, page_url, page_html))
            site_dir = pages_dir / host(url)
            site_dir.mkdir(parents=True, exist_ok=True)
            for i, (category, page_url, page_html) in enumerate(htmls):
                (site_dir / f"{i}_{category}.html").write_text(page_html, encoding="utf-8")
            (site_dir / "pages.json").write_text(json.dumps([[c, u] for c, u, _ in htmls], ensure_ascii=False), encoding="utf-8")

            raw_pages = [lines(h) for _, _, h in htmls]
            raw_words = sum(len(l.split()) for pg in raw_pages for l in pg)
            long_lines = {norm(l) for pg in raw_pages for l in pg if len(l.split()) >= LONG}
            variants = {
                "repeats": "\n".join(l for pg in drop_repeats(raw_pages) for l in pg),
                "traf": "\n".join(trafilatura.extract(h) or "" for _, _, h in htmls),
                "traf_recall": "\n".join(trafilatura.extract(h, favor_recall=True) or "" for _, _, h in htmls),
            }
            row = {"site": host(url), "pages": len(htmls), "raw_words": raw_words, "long_lines": len(long_lines)}
            for label, text in variants.items():
                (site_dir / f"clean_{label}.txt").write_text(text, encoding="utf-8")
                text_n = norm(text)
                kept = sum(1 for l in long_lines if l in text_n)
                row[label] = {"words": len(text.split()), "cut": 1 - len(text.split()) / max(raw_words, 1),
                              "kept": kept / len(long_lines) if long_lines else None}
            rows.append(row)
            cells = "  ".join(f"{label}: {row[label]['words']:5d} kelime (-%{row[label]['cut']*100:3.0f}) korunan={'-' if row[label]['kept'] is None else format(row[label]['kept']*100, '3.0f')+'%'}" for label in variants)
            print(f"{host(url):24} sayfa={len(htmls)} ham={raw_words:5d} içerik cümlesi={len(long_lines):3d} | {cells}")
        browser.close()
    (OUT / "trial_text_cleaning.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nÖZET")
    for label in ("repeats", "traf", "traf_recall"):
        cuts = [r[label]["cut"] for r in rows]
        kepts = [r[label]["kept"] for r in rows if r[label]["kept"] is not None]
        empty = sum(1 for r in rows if r[label]["words"] == 0)
        print(f"  {label:12} kısalma ortanca=%{statistics.median(cuts)*100:.0f} | korunan içerik ortanca=%{statistics.median(kepts)*100:.0f}, en kötü=%{min(kepts)*100:.0f} | boş dönen site={empty}")


if __name__ == "__main__":
    main()
