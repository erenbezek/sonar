"""Cyberpark şirket listesini indirir: ad, site adresi (varsa), sektör (varsa)."""
import html
import re
import time

import requests

from sitefind import OUT, USER_AGENT, ca_bundle

BASE = "https://www.cyberpark.com.tr/firma-arsiv"
CARD_RX = re.compile(
    r'<a(?P<attrs>[^>]*)>\s*<div class="e-bulletin-image-box.*?<h3[^>]*>(?P<name>.*?)</h3>\s*<p[^>]*>(?P<sector>.*?)</p>', re.S
)


def clean(s: str) -> str:
    return " ".join(html.unescape(s).split())


def main() -> None:
    bundle = ca_bundle()
    rows, page = [], 1
    while True:
        url = BASE if page == 1 else f"{BASE}/{page}"
        r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=60, verify=bundle)
        cards = list(CARD_RX.finditer(r.text))
        if r.status_code != 200 or not cards:
            break
        for m in cards:
            href = re.search(r'href="([^"]*)"', m["attrs"])
            rows.append((clean(m["name"]), href.group(1).strip() if href else "", clean(m["sector"])))
        if f'href="/firma-arsiv/{page + 1}"' not in r.text:
            break
        page += 1
        time.sleep(1)
    (OUT / "companies.tsv").write_text("\n".join("\t".join(row) for row in rows), encoding="utf-8")
    print(f"{len(rows)} şirket, {sum(1 for row in rows if row[1])} tanesinin adresi var ({page} sayfa)")


if __name__ == "__main__":
    main()
