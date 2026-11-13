"""Deneme 6: ilk kelimesi kısa olan şirketlerde site bulma.

Kural: kısa ilk kelime tek başına aranır, alan adının başında olmalı, site doğrulamadan geçmeli.
Örneklem: kısa ilk kelimeli ve adresi yazan 19 şirketten, deneme 5'te kullanılmayan 9'u.
Kriter (denemeden önce yazıldı): kabul edilen yanlış site 0, kabul edilen doğru site en az 5/9.
"""
import json
import random
import time

from playwright.sync_api import sync_playwright

from sitefind import (OUT, ca_bundle, choose, first_word, has_short_first_word, host, load_companies,
                      read_key, same_site, search, short_name, verify)


def main() -> None:
    api_key, bundle = read_key("TAVILY_API_KEY"), ca_bundle()
    pool = [c for c in load_companies() if has_short_first_word(c[0]) and c[1] and host(c[1])]
    random.seed(20261121)  # deneme 5'in örneklemi
    used = random.sample(pool, 10)
    sample = [c for c in pool if c not in used]
    print(f"havuz: {len(pool)} | deneme 5'te kullanılan: {[first_word(c[0]) for c in used]} | bu deneme: {len(sample)}")

    tally = {"accepted_right": 0, "accepted_other": 0, "rejected_right": 0, "rejected_other": 0, "not_found": 0}
    records = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for name, url, _sector in sample:
            want = host(url)
            results = search(short_name(name), api_key)
            time.sleep(1)
            rank, picked = choose(name, results)
            status = detail = ""
            if picked:
                status, detail = verify(picked, bundle, browser)
                key = ("accepted_" if status == "verified" else "rejected_") + ("right" if same_site(picked, want) else "other")
                tally[key] += 1
            else:
                tally["not_found"] += 1
            hosts = [host(r["url"]) for r in results]
            print(f"\n=== {short_name(name)[:60]}  (listede: {want}; aranan: {first_word(name)})")
            print(f"  seçilen: {picked} (sıra {rank}) {'AYNI' if picked and same_site(picked, want) else ('FARKLI' if picked else '-')} | {status} {detail}")
            print(f"  sonuçlar: {hosts}")
            records.append({"name": name, "listed": want, "picked": picked, "rank": rank, "status": status, "detail": detail, "results": hosts})
        browser.close()
    print(f"\nÖZET: {tally}  (n={len(sample)})")
    (OUT / "trial_short_first_word.json").write_text(json.dumps(records, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
