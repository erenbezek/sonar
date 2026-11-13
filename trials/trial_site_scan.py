"""Deneme 9: site scan sayfaları nasıl seçip okumalı (Groq yok).

Kriter (denemeden önce yazıldı):
- 50 kelime kuralı, içeriği JavaScript ile gelen siteleri kaçırmamalı (0 site). Tanım: tarayıcıda en az 100 kelime
  ve düz okumanın en az 5 katı.
- 50 kelime kuralı en fazla 2 sitede gereksiz yere Playwright açtırmalı.
- Seçilen ürün sayfası, ürün sayfası olan sitelerin en az %80'inde gerçekten ürün ya da hizmet sayfası olmalı (elle bakılır).
"""
import json
import random

from playwright.sync_api import sync_playwright

from sitefind import OUT, ca_bundle, host, load_companies
from sitescan import BROWSER_THRESHOLD, get, parse, read_home, render, select_pages

# Sitesi daha önce okunan şirketler (FINDINGS bölüm 1-4, 11).
SEEN = {"karel.com.tr", "endeksa.com", "kaminovasyon.com", "teslakom.com", "meteksan.com", "ctech.com.tr", "melsis.com.tr", "solveka.com.tr",
        "gelisimpark.com.tr", "sentebiolab.com.tr", "ekin.tc", "aeros.com.tr", "connected2.me", "nanodev.com.tr", "adhocteknoloji.com",
        "en.simovate.com", "atekmidas.com", "thorvacs.com", "unam.bilkent.edu.tr", "argemyazilim.com.tr", "polaran.com", "apinizer.com",
        "maarifa.com.tr", "comnify.tech", "kron.com.tr", "akdogan.tech", "kmo.com.tr", "dusoft.com.tr", "agem.com.tr", "teknokar.com"}


def main() -> None:
    bundle = ca_bundle()
    pool = [c for c in load_companies() if c[1] and host(c[1]) and host(c[1]) not in SEEN]
    random.seed(20261124)
    sample = random.sample(pool, 15)
    records = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for name, url, sector in sample:
            final, html, note = read_home(url, bundle)
            text, links = parse(html)
            plain_words = len(text.split())
            b_final, b_html = render(browser, final or (url if "//" in url else "http://" + url))
            b_text, b_links = parse(b_html)
            browser_words = len(b_text.split())
            js_site = browser_words >= 100 and browser_words >= 5 * max(plain_words, 1)
            rule_browser = plain_words < BROWSER_THRESHOLD
            use_links, base = (b_links, b_final) if rule_browser and b_html else (links, final)
            picks = select_pages(base, use_links) if base else {}
            print(f"\n=== {name[:50]}  ({host(url)}; sektör: {sector[:35] or '-'}) {note}")
            print(f"  ana sayfa: düz={plain_words} kelime, tarayıcı={browser_words} kelime | JS sitesi={js_site} | kural tarayıcı açar={rule_browser}")
            menu = []
            for _, t in use_links:
                t = t[:26]
                if t and len(t.split()) <= 4 and t not in menu:
                    menu.append(t)
            print("  kısa bağlantı metinleri:", " | ".join(menu[:38])[:560])
            record = {"name": name, "url": url, "plain_words": plain_words, "browser_words": browser_words, "js_site": js_site,
                      "rule_browser": rule_browser, "note": note, "picks": {}}
            for category, items in picks.items():
                for page_url, link_text, score in items:
                    _, page_html = (render(browser, page_url) if rule_browser else get(page_url, bundle))
                    page_text, _ = parse(page_html)
                    words = len(page_text.split())
                    print(f"  {category:8} [{link_text[:30]}] {page_url[:75]} puan={score:.1f} kelime={words}")
                    print(f"           {' '.join(page_text.split()[40:75])[:230]}")
                    record["picks"].setdefault(category, []).append({"url": page_url, "text": link_text, "words": words})
            records.append(record)
        browser.close()
    (OUT / "trial_site_scan.json").write_text(json.dumps(records, ensure_ascii=False, indent=1), encoding="utf-8")
    js = [r for r in records if r["js_site"]]
    print(f"\nÖZET: JS sitesi={len(js)} | kuralın kaçırdığı JS sitesi={sum(1 for r in js if not r['rule_browser'])} | "
          f"gereksiz tarayıcı={sum(1 for r in records if r['rule_browser'] and not r['js_site'])} | "
          f"ürün sayfası seçilen={sum(1 for r in records if r['picks'].get('product'))}/{len(records)}")


if __name__ == "__main__":
    main()
