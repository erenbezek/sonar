"""Deneme 8: iki adımlı arama + sıkı doğrulama, yeni şirketlerde.

Kriter (denemeden önce yazıldı):
- Adresi bilinen 10 yeni şirkette kabul edilen doğru site en az 7/10.
- Kabul edilen yanlış site 0 (iki grupta da).
- Sıkı doğrulamanın elediği doğru site en fazla 1.
Listedekinden farklı çıkan adresler elle kontrol edilir.
"""
import json
import random

from playwright.sync_api import sync_playwright

from sitefind import OUT, ca_bundle, find_site, first_word, has_short_first_word, host, load_companies, read_key, same_site, short_name

# Önceki site bulma denemelerinde kullanılan şirketler (FINDINGS bölüm 7-15).
USED_HOSTS = {
    "bilgeadam.com", "tomboprint.com", "yazilimparki.com.tr", "dakikyazilim.com", "vektora.com", "anser.com.tr", "smartict.com.tr",
    "infinia.com.tr", "simsoft.com.tr", "emvop.com", "agem.com.tr", "kimola.com", "oska.com.tr", "rekrom.com", "pleksus.com.tr",
    "omegabigdata.com", "smayd.com", "mobiliz.com.tr", "birfatura.com", "codebase.com.tr", "comnify.tech", "openzeka.com",
    "innology.com.tr", "aipaturkey.org", "figensoft.com", "limakteknoloji.com", "oplog.com.tr", "fabric-ate.com", "mobiltrust.com",
    "seneka.com.tr", "creasaur.net", "harp.com.tr", "elektroniksavunma.com", "antenom.com", "turkai.com", "adim.tech",
    "datateam.com.tr", "iliksoft.com", "finkoto.com",
}
USED_NAMES = ("İNOVED", "BULBİ", "AI GENERATOR", "E KAMPÜS", "CURVE", "DAİİCHİ", "HD YAPIMCILIK", "FORECR", "HEARTSAPİENS", "MAVENSİS",
              "AREKA", "ZİRONSOFT", "NEDMOD", "TROPIQ", "ORBİTEL", "TUĞÇE", "VISIONX", "SECUNNİX", "EKİPTESİN", "AHMET FARUK", "FİNPRECİA")


def main() -> None:
    api_key, bundle = read_key("TAVILY_API_KEY"), ca_bundle()
    companies = [c for c in load_companies() if not c[0].startswith(USED_NAMES)]
    known_pool = [c for c in companies if c[1] and host(c[1]) and host(c[1]) not in USED_HOSTS and not has_short_first_word(c[0])]
    unknown_pool = [c for c in companies if not c[1]]
    random.seed(20261122)
    known = random.sample(known_pool, 10)
    random.seed(20261123)
    unknown = random.sample(unknown_pool, 10)
    print(f"adresi bilinen havuz: {len(known_pool)} | adresi olmayan havuz: {len(unknown_pool)}")
    records = {"known": [], "unknown": []}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for group, sample in (("known", known), ("unknown", unknown)):
            print(f"\n######## {'ADRESİ BİLİNEN' if group == 'known' else 'ADRESİ OLMAYAN'} 10 ŞİRKET")
            for name, url, sector in sample:
                want = host(url) if url else ""
                result = find_site(name, api_key, bundle, browser)
                print(f"\n=== {short_name(name)[:60]}  (listede: {want or '-'}; aranan: {first_word(name)}; sektör: {sector[:30] or '-'})")
                for step in result["steps"]:
                    mark = ""
                    if step["picked"] and want:
                        mark = "AYNI" if same_site(step["picked"], want) else "FARKLI"
                    in_results = next((i + 1 for i, h in enumerate(step["results"]) if want and same_site(h, want)), None)
                    print(f"  {step['step']:10} seçilen={step['picked']} (sıra {step['rank']}) {mark} | {step['status']} {step['detail']} | listedeki site sırası={in_results}")
                print(f"  KABUL: {result['accepted']}")
                records[group].append({"name": name, "listed": want, **result})
        browser.close()
    (OUT / "trial_two_step.json").write_text(json.dumps(records, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
