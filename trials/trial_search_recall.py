"""Deneme 7: aramanın kaçırdığı şirketlerde ikinci sorgu ve daha fazla sonuç işe yarıyor mu.

Örneklem: önceki denemelerde doğru sitesi ilk 5 sonuca girmeyen, adresi bilinen 10 şirket.
Her şirket için iki sorgu (10 sonuç): sadece ad, ad + "Ankara".
Kriter (denemeden önce yazıldı): bir yöntem, ad/ilk 5'e göre en az 4 şirket fazla bulursa işe yarıyor sayılır;
kabul edilen yanlış site 0 olmalı.
"""
import json
import time

from playwright.sync_api import sync_playwright

from sitefind import OUT, ca_bundle, choose, first_word, host, load_companies, read_key, same_site, search, short_name, verify

MISSED = ["FDN SOFT", "İLG BİLİŞİM", "BK MOBİL", "A2 TEKNOLOJİ", "C TECH", "C.B.K. SOFT", "CE TASARIM", "E-A TEKNOLOJİ", "CODEBASE", "REKROM"]


def main() -> None:
    api_key, bundle = read_key("TAVILY_API_KEY"), ca_bundle()
    companies = load_companies()
    sample = [next(c for c in companies if c[0].startswith(prefix)) for prefix in MISSED]
    variants = {"name/5": ("name", 5), "name/10": ("name", 10), "ankara/5": ("ankara", 5), "ankara/10": ("ankara", 10)}
    in_results = dict.fromkeys(variants, 0)
    accepted_right = dict.fromkeys(variants, 0)
    accepted_other = dict.fromkeys(variants, 0)
    verified_cache: dict[str, tuple[str, str]] = {}
    records = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for name, url, _sector in sample:
            want, query = host(url), short_name(name)
            found = {"name": search(query, api_key, 10)}
            time.sleep(1)
            found["ankara"] = search(query + " Ankara", api_key, 10)
            time.sleep(1)
            print(f"\n=== {query[:55]}  (listede: {want}; aranan: {first_word(name)})")
            record = {"name": name, "listed": want}
            for label, (source, limit) in variants.items():
                results = found[source][:limit]
                hosts = [host(r["url"]) for r in results]
                listed_rank = next((i + 1 for i, h in enumerate(hosts) if same_site(h, want)), None)
                in_results[label] += listed_rank is not None
                rank, picked = choose(name, results)
                status = ""
                if picked:
                    if picked not in verified_cache:
                        verified_cache[picked] = verify(picked, bundle, browser)
                    status = verified_cache[picked][0]
                    if status == "verified":
                        if same_site(picked, want):
                            accepted_right[label] += 1
                        else:
                            accepted_other[label] += 1
                print(f"  {label:10} listedeki site sırası={listed_rank}  seçilen={picked} {status}")
                record[label] = {"listed_rank": listed_rank, "picked": picked, "status": status}
            for source in ("name", "ankara"):
                print(f"  {source:7} sonuçlar: {[host(r['url']) for r in found[source]]}"[:330])
            records.append(record)
        browser.close()
    print("\nÖZET (10 şirket)")
    for label in variants:
        print(f"  {label:10} listedeki site sonuçlarda={in_results[label]}  kabul edilen doğru={accepted_right[label]}  kabul edilen farklı={accepted_other[label]}")
    (OUT / "trial_search_recall.json").write_text(json.dumps(records, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
