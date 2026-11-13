# trials

Karar vermeden önce gerçek şirketlerde yapılan denemelerin betikleri. Sonuçlar `docs/FINDINGS.md`'de.

- `sitefind.py`: site bulma yönteminin ortak parçaları (kısa ad, Tavily araması, seçim kuralı, doğrulama).
- `cyberpark_list.py`: Cyberpark şirket listesini indirip `out/companies.tsv` dosyasına yazar.
- `sitescan.py`: site scan'in ortak parçaları (sayfayı okuma, metni çıkarma, okunacak sayfaları seçme, tekrar eden satırı atma).
- `trial_*.py`: tek tek denemeler. Her dosyanın başında denemenin kriteri yazar.

Çalıştırma:

```
python3 -m venv .venv
.venv/bin/pip install requests playwright trafilatura
.venv/bin/playwright install chromium-headless-shell
.venv/bin/python trials/cyberpark_list.py
.venv/bin/python trials/trial_short_first_word.py
```

Anahtarlar `.env/keys` dosyasından okunur (`TAVILY_API_KEY=...`). İndirilen sayfalar ve ham sonuçlar `trials/out/` altına yazılır, repoya girmez.
