# FINDINGS

Gerçek şirket sitelerini inceleyerek çıkan bulgular. Kararlar `DECISIONS.md`'de durur, burada sadece ölçülen şeyler var.
Her denemede kriter sonuçtan önce yazıldı.

## Örneklem

- Cyberpark listesi (2026-11-13): 368 şirket. 154'ünün (%42) site adresi yazıyor, 172'sinin sektör bilgisi var.
- Örneklem 1: listeden rastgele 10 şirket (seed 20261112) + Cerebrum Tech. Toplam 11 site.
- Örneklem 2: listeden rastgele 10 yeni şirket (seed 20261113), site adresi yazanlar arasından.
- Bu 21 şirket tasarımda kullanıldı, test setine giremez.

## 1. Site okuma (2026-11-13)

Her siteden düz HTTP isteğiyle en fazla 4 sayfa okundu: ana sayfa, ürün, hakkımızda, kariyer.

| Kriter | Sonuç |
|---|---|
| Menü kelimeleri (ürün, çözüm, hizmet, product, solution, service) sitelerin en az %80'inde ürün sayfasını bulmalı | Tutmadı: 8/11 |
| İçeriği olan hiçbir site düz okumada 200 kelimenin altında kalmamalı | Tutmadı: Endeksa 0 kelime |

- Bazı sitelerde ürün menüsünün adresi yok, sadece alt menüyü açıyor (Teslakom, CTech).
- Ürün içeriği tek sayfada değil: Karel'de 43, CTech'te 24, Meteksan'da 13 ürün bağlantısı var.
- KAM İnovasyon'un sitesi 197 kelime ama 9 web platformu olan bir yazılım şirketi. 200 kelimelik eşik onu yanlış işaretlerdi.
- Site adresini addan tahmin etmek güvenilmez: `cerebrumtech.com` satılık alan adı, gerçek adres `cerebrumtechnologies.com`.

## 2. Kelime eşleştirme (2026-11-13)

Örneklem 1'de sinyal kelimeleri sayfa metninde arandı.

| Sinyal | Kelimenin geçtiği site | Gerçekten doğru olan |
|---|---|---|
| Yapay zekâ | 1 | 1 (Cerebrum) |
| Docker, Kubernetes, CI/CD | 0 | 0 |
| Bulut | 3 | Şirketin nasıl çalıştığını gösteren yok (ürün adı, blog yazısı) |
| Backend teknolojisi | 4 | 0 ("Kariyer.net", menüdeki "API", gömülü yazılım için "C#, Python") |
| Remote | 1 | 0 ("hibrit haberleşme") |

- Şirketler kullandıkları teknolojiyi sitede yazmıyor. 21 sitenin hiçbirinde Docker, Kubernetes ya da CI/CD geçmedi.
- "Yazılım" kelimesi de ayırt etmiyor: Cerebrum'da hiç geçmiyor, dağıtıcı olan Teslakom'da 10 kez geçiyor.
- Sonuç: kelime eşleştirmeyle fit score hesaplanamaz.
- Ürün sayfası fikri tek örnekte doğrulandı: Cerebrum'un ana sayfasında slogan, çözümler sayfasında somut ürün (Cere LLM) var.

## 3. Groq ile olgu çıkarma, deneme 1 (2026-11-13)

Örneklem 1, model `openai/gpt-oss-120b`, sıcaklık 0. Sorular: ne iş yapıyor, yazılım türü (server_web, embedded, both, none, unknown), üründe yapay zekâ.

| Kriter | Sonuç |
|---|---|
| Kanıt cümlesi sayfada birebir geçmeli | Tutmadı: 20 kanıttan 3'ü bulunamadı (2'si tire ve görünmez karakter farkı, 1'i sayfada yok) |
| Yazılım türü elle etiketle aynı, en az 9/11 | Tutmadı: 8/11 |
| Üründe yapay zekâ doğru, en az 10/11 | Tuttu: 11/11 |
| Boş gelen Endeksa'ya "bilinmiyor" demeli | Tuttu |

- Üç hata da "both" cevabıydı. Teslakom'da sattığı yazılımı geliştirdiği yazılım saydı.
- "Ne iş yapıyor" alanı okunan 10 sitede de doğru özet verdi.

## 4. Groq ile olgu çıkarma, deneme 2 (2026-11-13)

Örneklem 2. Soru basitleştirildi: "kendi yazılımını geliştiriyor mu" (yes, no, unknown) ve türü kısa not olarak. Satmak ile geliştirmek ayrımı soruya eklendi. Kanıt kontrolünde tire, görünmez karakter, boşluk ve büyük-küçük harf farkı yok sayıldı.

| Kriter | Sonuç |
|---|---|
| Kanıt cümlesi sayfada geçmeli | Tuttu: 12/12 |
| "Kendi yazılımını geliştiriyor mu" elle etiketle aynı, en az 9/10 | Tuttu: 10/10 |
| Üründe yapay zekâ doğru, en az 9/10 | Tuttu: 10/10 |
| Okunamayan şirkete "bilinmiyor" demeli | Tuttu: 4/4 |

Bu sonucun sınırları:
- Örneklem kolaydı. 4 şirket okunamadı, okunan 6'nın 4'ü açıkça yazılım dışıydı.
- "Satıyor mu, geliştiriyor mu" belirsizliği olan şirket çıkmadı, o ayrım sınanmadı.
- Üründe yapay zekâ olan şirket çıkmadı.
- Bazı kanıtlar sayfada var ama konuyla ilgisi zayıf.

## 5. Groq kotası (2026-11-13, Groq'un kendi cevabından)

- `openai/gpt-oss-120b`: günde 1.000 istek, dakikada 8.000 token.
- Türkçe metinde kelime başına yaklaşık 2,9 token. 2.500 kelimelik bir şirket dakikalık kotayı dolduruyor: pratikte dakikada 1 şirket.
- Günlük token sınırı doğrulanmadı.
- Kota anahtara değil hesaba bağlı (doğrulanmadı).

## 6. Okunamayan siteler (2026-11-13)

Site adresi yazan 20 şirketin 5'i ilk okumada okunamadı.

| Şirket | Sebep | Basit yöntemle kurtuldu mu |
|---|---|---|
| Simovate | Listedeki adres (`en.simovate.com`) çalışmıyor | Evet: ana alan adı açılıyor (396 kelime) |
| Argem | Ana sayfa yönlendirme sayfası | Evet: yönlendirme izlenince açılıyor (227 kelime) |
| Nanodev | İçerik JavaScript ile yükleniyor | Kısmen: sayfanın açıklama etiketinde tek cümle var |
| Endeksa | İçerik JavaScript ile yükleniyor | Hayır |
| Ekin | Alan adı artık yok | Hayır |

- Kurtulan iki şirket de yazılım şirketi (Argem: web framework ve ERP, Simovate: simülasyon yazılımı). Okunamayan site, ilgisiz şirket demek değil.

## Kabaca hesap

368 şirket → 154'ünün sitesi yazıyor → yaklaşık 115-130'u okunabiliyor → okunabilenlerin yaklaşık yarısı kendi yazılımını geliştiriyor. 20 şirketlik örneklemden geldiği için yanılma payı geniş. Site adresi yazmayan 214 şirket hakkında henüz veri yok.

## 7. Tavily ile site adresi bulma, deneme 1 (2026-11-13)

Adresi listede yazan şirketlerden rastgele 10 tane (seed 20261114). Her şirket iki sorguyla arandı: listedeki tam ad ve tam ad + "Bilkent Cyberpark". Sorgu başına 5 sonuç.

| Kriter | Sonuç |
|---|---|
| Doğru site ilk 3 sonuçta, 10 şirketin en az 7'sinde (iki sorgudan biriyle) | Tutmadı: 5/10 |
| Teknokentli sorgu sade sorgudan en az 2 şirket fazla bulmalı | Tutmadı: sade 3/10, teknokentli 4/10 |

- Sonuçları rehber siteleri dolduruyor: LinkedIn, RocketReach, PitchBook, Yahoo Finance, Instagram.
- Teknokent adı eklemek 3 şirkette sırayı iyileştirdi, 1 şirkette doğru siteyi sonuçlardan düşürdü. 10 şirketle kesin bir şey söylenemez.
- Örneklemde kusur: bir şirketin (İnoved) listedeki adresi okunamadı, o şirket hiçbir sorguyla "bulundu" sayılamazdı.
- Listedeki adres her zaman şirketin kendi alan adı değil: BGTS için listede `bilgeadam.com` yazıyor, aramada `bgts.com` çıktı. Yazılım Parkı için listede `yazilimparki.com.tr`, aramada `yazilimparki.com` çıktı. Bunlar kriterde "bulunamadı" sayıldı.
- Sorguda şirketin tam ticari unvanı kullanıldı ("... ANONİM ŞİRKETİ"). Kısa adla denenmedi.

## 8. Tavily ile site adresi bulma, deneme 2 (2026-11-13)

Yeni 10 şirket (seed 20261115). Değişiklikler: unvandaki hukuki ekler atıldı ("A.Ş.", "LİMİTED ŞİRKETİ", "SANAYİ VE TİCARET"), 14 rehber sitesi aramadan dışlandı (LinkedIn, RocketReach, PitchBook vb.). Sade ve "Bilkent Cyberpark" ekli sorgu karşılaştırıldı.

| Kriter | Sonuç |
|---|---|
| Doğru site ilk 3 sonuçta, en az 7/10 | Tutmadı: 3/10 |
| Teknokentli sorgu sade sorgudan en az 2 şirket fazla bulmalı | Tutmadı: sade 3/10, teknokentli 2/10 |

- Doğru site çoğunlukla sonuçlarda var ama üst sırada değil. İlk 5 sonuca bakılırsa: sade sorgu 9/10, teknokentli sorgu 5/10.
- Teknokent adı eklemek bu denemede zarar verdi: sonuçlara `cyberpark.com.tr` ve başka teknopark rehberleri doldu, 4 şirkette doğru site ilk 5'ten düştü.
- İki denemenin toplamında teknokent adı eklemenin faydası görülmedi.
- İlk 5 sonuç içinde doğru site, çoğunlukla alan adında şirket adının ayırt edici kelimesi geçen sonuçtu (emvop.com, kimola.com, smayd.com). Bu, sonuçlara bakarak çıkarılmış bir varsayım, ayrıca sınanmadı.
- Kusur: unvan kısaltma "LTD.ŞTİ." (boşluksuz) yazımını yakalamadı, AGEM tam unvanla arandı.
- Sonuçlarda açıklanamayan `tavily.com` adresleri çıktı, incelenmedi.

## 9. Tavily ile site adresi bulma, deneme 3 (2026-11-13)

Sade sorgu (kısa ad), ilk 5 sonuç. Seçim kuralı: alan adında şirket adının ilk kelimesi geçen ilk sonuç; yoksa "bulunamadı". Listedekinden farklı adres seçilirse sayfa açılıp aynı şirket mi diye bakıldı (kural denemeden önce yazıldı).

Bölüm 1, adresi bilinen 10 yeni şirket (seed 20261116):

| Kriter | Sonuç |
|---|---|
| Kural doğru siteyi seçmeli, en az 7/10 | Tuttu: 8/10 |
| Kural en fazla 1 yanlış site seçmeli | Tuttu: 1 yanlış |

- Doğru sayılan 8'in biri listedekinden farklı adresti: `oplog.io`. Listedeki `oplog.com.tr` zaten oraya yönleniyor.
- Yanlış seçim: Codebase için yabancı bir şirketin sitesi (`codebase.com`) seçildi, doğrusu `codebase.com.tr`.
- Bulunamayan: "Yapay Zeka Politikaları Derneği (AIPA)". Doğru site ilk sıradaydı ama alan adı kısaltmadan geliyor (`aipaturkey.org`).

Bölüm 2, adresi olmayan 10 şirket (seed 20261117). Doğru cevap bilinmediği için seçilen siteler elle kontrol edildi:

| Sonuç | Sayı | Şirketler |
|---|---|---|
| Büyük ihtimalle doğru | 6 | Bulbi, E Kampüs, Curve, Daiichi, Forecr, HeartSapiens |
| Yanlış | 1 | AI Generator için `fal.ai` seçildi |
| Büyük ihtimalle yanlış | 1 | Areka Yazılım için İstanbul'daki bir makine üreticisi seçildi |
| Bulunamadı | 2 | HD Yapımcılık, Mavensis |

- Kuralın zayıf yeri kısa ilk kelimeler: "AI", "E", "HD". "AI" yanlış siteyi seçtirdi, "E" tesadüfen doğruyu seçti.
- Sınanmamış gözlem: doğru sitelerin sayfasında "Cyberpark", "Bilkent" ya da "Ankara" geçiyor (Oplog, Codebase'in doğru sitesi). Yanlış seçilen `codebase.com`'da geçmiyor. Teknokent adı sorguda işe yaramadı, ama bulunan siteyi doğrulamakta işe yarayabilir.

## 10. Tavily ile site adresi bulma, deneme 4 (2026-11-13)

Deneme 3'e iki kural eklendi: (1) ilk kelime 4 harften kısaysa ilk iki kelime birleştirilip aranır, (2) seçilen sitenin ana sayfasında, yoksa iletişim sayfasında "Cyberpark", "Bilkent" ya da "Ankara" geçmeli; geçmiyorsa site kabul edilmez. `cyberpark.com.tr` aramadan dışlandı.

Bölüm 1, adresi bilinen 10 yeni şirket (seed 20261118):

| Kriter | Sonuç |
|---|---|
| Kabul edilen yanlış site: 0 | Tuttu: 0 |
| Kabul edilen doğru site: en az 6/10 | Tuttu: 7/10 |

- Doğrulama 1 doğru siteyi eledi (Harp Savunma: iletişim sayfası bulunamadı) ve listedekinden farklı 1 siteyi eledi (Creasaur için `creasaur.com`; listede `creasaur.net`, aynı şirket olup olmadığı belirsiz).
- 1 şirket bulunamadı: listedeki adresinde şirket adı geçmiyor (ARMS → `elektroniksavunma.com`).
- Kabul edilen 7 sitenin 5'i sadece "Ankara" kelimesiyle doğrulandı.
- Kural (1) sınanmadı: örneklemde ilk kelimesi 4 harften kısa şirket çıkmadı.

Bölüm 2, adresi olmayan 10 yeni şirket (seed 20261119), elle kontrol:

| Sonuç | Sayı | Şirketler |
|---|---|---|
| Kabul edildi, doğru görünüyor | 3 | ZironSoft, Tropiq, VisionX |
| Seçildi ama doğrulanmadı | 2 | Nedmod (sayfa neredeyse boş), Orbitel (iletişim sayfasında şehir yok) |
| Bulunamadı | 5 | İkisi şahıs adı (şirket değil, kişi adına kayıt) |

- Doğrulama kuralıyla yanlış site kabul edilmedi, ama adresi olmayan şirketlerde verim düştü: deneme 3'te 10'da yaklaşık 6, bu denemede 10'da 3.
- Doğrulanmayan iki site büyük ihtimalle doğru şirketti. Bunlar atılmamalı, "doğrulanmamış aday" olarak tutulmalı.
- Kabaca hesap: adresi olmayan 214 şirketin %30-50'si bu yöntemle kazanılabilir. Dört denemede toplam 80 Tavily kredisi harcandı.

## 11. Groq ile olgu çıkarma, deneme 3: zor şirketler (2026-11-13)

Listede sektöründe danışmanlık, telekomünikasyon ya da entegrasyon geçen ve adresi yazan şirketler: tam 10 tane çıktı, hepsi alındı. Soru metni deneme 2 ile aynı.

| Kriter | Sonuç |
|---|---|
| Kanıt cümlesi sayfada geçmeli: hepsi | Tutmadı: 14/15 |
| "Kendi yazılımını geliştiriyor mu" elle etiketle aynı, en az 8/10 | Tuttu: 9/10 |
| Sadece satan şirkete "geliştiriyor" demesi: en fazla 1 | Tuttu, ama sınanmadı: örneklemde sadece satan şirket çıkmadı |
| Okunamayan şirkete "bilinmiyor" demeli | Tuttu: 3/3 |

- Bulunamayan kanıt (Akdoğan): model cümlenin öznesini değiştirdi. Sayfada "They are operational building blocks", modelde "Our products are operational building blocks". Kanıt kontrolü bu tür değişikliği yakalıyor.
- Tek fark (Polaran): 59 kelimelik sayfada "kutupsal kodlama ile ilgili ürün ve fikri mülkiyet geliştirme" yazıyor, yazılım kelimesi geçmiyor. Model "yes (software library)" dedi: metnin ötesine geçen bir çıkarım.
- Ek kontrol, kriter dışı: deneme 1'de yanıltan Teslakom yeni soruyla tekrar soruldu. Model yine "yes" dedi, kanıt olarak şirketin sunduğu ürünleri anlatan bir cümle gösterdi. Soruya eklenen "satmak geliştirmek sayılmaz" cümlesi, tasarlandığı örnekte bile işe yaramadı. Teslakom'un sitesinde ayrıca "Yazılım Geliştirme" başlığı da var; şirketin gerçekte yazılım geliştirip geliştirmediği siteden kesin anlaşılmıyor.
- Okunamayan 3 site: Comnify (içerik JavaScript ile yükleniyor), Kron (bağlantı zaman aşımı), KMO (bot doğrulama sayfası).
- Önceki "şirketler teknolojiyi sitede yazmıyor" bulgusuna iki karşı örnek: Akdoğan'ın hizmet menüsünde "Backend Development, CI/CD, Amazon Web Services, Microservices Architecture" var. Dusoft'un ana sayfasında "WE ARE HIRING Developer C#, PYTHON, JAVA ... FRONTEND - BACKEND" yazıyor. İkisi de 31 site içinde.
- Bu "zor" örneklem beklenenden kolaydı: okunabilen 7 şirketin 5'i açıkça yazılım şirketi. Sektör alanındaki "danışmanlık" kelimesi çoğunlukla yazılım şirketlerinin unvanından geliyor.

## 12. Okunamayan sitelerde Playwright ve Tavily extract (2026-11-13)

Adresi yazan 30 şirketin 8'i ilk düz okumada okunamamıştı. İkisi basit kurallarla kurtulmuştu (bölüm 6). JavaScript ile yüklenen 3 site (Endeksa, Nanodev, Comnify) ve zaman aşımına uğrayan Kron'da üç yöntem denendi. Playwright 1.65.1, headless Chromium, varsayılan tarayıcı kimliği.

| Kriter | Sonuç |
|---|---|
| JavaScript ile yüklenen 3 sitede Playwright şirketin işini anlatan metni getirmeli (en az 100 kelime): en az 2/3 | Tuttu: 2/3 |
| Aynı 3 sitede Tavily extract aynı metni getirmeli: en az 2/3 | Tutmadı: 0/3 |

| Site | Düz okuma | Playwright | Tavily extract |
|---|---|---|---|
| Nanodev | 5 kelime | 228 kelime, 17 sn | Başarısız |
| Comnify | 1 kelime | 111 kelime, 2 sn | Başarısız |
| Endeksa | 0 kelime | Cloudflare bot doğrulama sayfası | Başarısız |
| Kron | Zaman aşımı | Zaman aşımı | Zaman aşımı |

- Tavily extract varsayılan ayarla denendi; "advanced" seçeneği denenmedi.
- KMO bot doğrulama sayfası gösterdiği için denenmedi. Bot doğrulamasını aşmaya çalışılmıyor.
- 8 okunamayan sitenin son durumu: 4'ü kurtuldu (Simovate: ana alan adı, Argem: yönlendirme, Nanodev ve Comnify: Playwright). 4'ü kaldı (Endeksa ve KMO: bot koruması, Kron: zaman aşımı, Ekin: alan adı kapanmış).
- Adresi yazan 30 şirkette okunamayan oran %27'den %13'e iniyor.
- Düz okumada kelime sayıları: JavaScript ile yüklenen sitelerde 0, 1, 5. İçeriği gerçekten az olan sitelerde 15-59. Playwright'a ne zaman başvurulacağını belirleyen eşik sınanmadı.

## 13. Site bulma, deneme 5: kısa ilk kelime ve Playwright'lı doğrulama (2026-11-13)

Bölüm A. Listede ilk kelimesi 4 harften kısa olan 47 şirket var, 19'unun adresi yazıyor. Bunlardan rastgele 10'u (seed 20261121). Kural: ilk iki kelime birleştirilip alan adında aranır ("T2 YAZILIM" → "t2yazilim").

| Kriter | Sonuç |
|---|---|
| Kabul edilen yanlış site: 0 | Tuttu: 0 |
| Kabul edilen doğru site: en az yarısı | Tutmadı: 3/10 |

- 7 şirket bulunamadı. Kural fazla sıkı: alan adları çoğunlukla iki kelimenin birleşimi değil (`t2.com.tr`, `kmo.com.tr`, `a2labs.com.tr`). 3 şirkette doğru site ilk 5 sonuçtaydı ama kural eşleştiremedi.
- Kabul edilen 3 sitenin 2'si listedekinden farklı adresti. Mil Yazılım: listedeki `miloyun.com` artık açılmıyor, bulunan `milyazilim.com.tr` doğru şirket (sayfada "Bilkent Cyberpark'ta faaliyet" yazıyor). Zeg Teknoloji: listede `egyazilim.com`, bulunan `zegteknoloji.com`; ad uyuyor ve sayfada Ankara geçiyor, ama iki site de düz okumada boş geldiği için elle tam doğrulanamadı.
- Listedeki adresler eskimiş olabiliyor. Arama bazen listeden daha güncel adres veriyor.

Kriter dışı, kuralın çıkış örnekleri: AI Generator, E Kampüs ve HD Yapımcılık üçünde de site seçilmedi. AI Generator'da artık yanlış site seçilmiyor. E Kampüs'te deneme 3'te bulunan doğru site bu sefer arama sonuçlarında hiç çıkmadı: aynı sorgu farklı zamanda farklı sonuç verebiliyor.

Bölüm B. Daha önce doğrulanamayan 3 sitede, düz okumada teknokent ya da şehir adı bulunamazsa sayfa Playwright ile açılıp tekrar arandı (kriter yok, gözlem):

| Site | Sonuç |
|---|---|
| Harp Savunma | Doğrulandı (Playwright, ana sayfada "Ankara") |
| Nedmod | Doğrulandı (Playwright, ana sayfada "Bilkent") |
| Orbitel | Doğrulanmadı (Playwright ile 88 kelime, şehir adı yok) |

## 14. Site bulma, deneme 6: kısa ilk kelime, yeni kural (2026-11-13)

Kural: kısa ilk kelime tek başına aranır, alan adının başında olmalı, site doğrulamadan geçmeli. Örneklem: kısa ilk kelimeli ve adresi yazan 19 şirketten deneme 5'te kullanılmayan 9'u. Betik: `trials/trial_short_first_word.py`.

| Kriter | Sonuç |
|---|---|
| Kabul edilen yanlış site: 0 | Tuttu: 0 |
| Kabul edilen doğru site: en az 5/9 | Tutmadı: 3/9 |

- Bulunamayan 4 şirketin hiçbirinde doğru site arama sonuçlarında yoktu (C Tech, C.B.K. Soft, CE Tasarım, E-A Teknoloji). Darboğaz seçim kuralı değil, aramanın kendisi: kısa ve genel adlarla yapılan sorgu ilgisiz sonuç getiriyor.
- Doğru site sonuçlarda olan 4 şirketin 4'ünü kural seçti, 3'ü doğrulandı.
- Doğrulanamayan doğru site (Map): `mapyazilim.com` sadece `www` ile açılıyor, doğrulama adımı `www`'suz adresi deniyordu. Betikteki hata düzeltildi, düzeltmeden sonra site doğrulandı. Kriter sonucu 3/9 olarak kalır; düzeltmeyle 4/9.
- Yabancı bir şirketin sitesi seçildi ama doğrulama eledi (Zeo için `zeotechnologies.com`).
- İki denemenin toplamı: ilk kelimesi kısa olan 19 şirketin 6-7'sinde doğru site kabul edildi, yanlış site kabul edilmedi. Listede bu türden 47 şirket var (%13).

## 15. Site bulma, deneme 7: aramanın kaçırdığı şirketler (2026-11-13)

Örneklem: önceki denemelerde doğru sitesi ilk 5 sonuca girmeyen, adresi bilinen 10 şirket (daha önce görülmüş şirketler, sonuç iyimser olabilir). Her şirket iki sorguyla, 10'ar sonuçla arandı: sadece ad ve ad + "Ankara". Betik: `trials/trial_search_recall.py`.

| Kriter | Sonuç |
|---|---|
| Bir yöntem, ad/ilk 5'e göre en az 4 şirket fazla bulmalı | Tutmadı: en iyi yöntem 3 fazla buldu |
| Kabul edilen yanlış site: 0 | Kesin yanlış yok; 1 site yanlış sebeple doğrulandı |

Doğru sitesi kabul edilen şirket sayısı (listedekinden farklı ama aynı şirkete ait adresler elle kontrol edilip doğru sayıldı):

| Yöntem | Doğru site kabul edildi |
|---|---|
| Ad, ilk 5 sonuç | 3/10 |
| Ad, ilk 10 sonuç | 4/10 |
| Ad + "Ankara", ilk 5 sonuç | 3/10 |
| Ad + "Ankara", ilk 10 sonuç | 6/10 |

- Bu 10 şirket daha önce "bulunamadı" çıkmıştı; bu çalışmada temel yöntem 3'ünü buldu. Sebep: arama sonuçları çalışmadan çalışmaya değişiyor ve iki şirkette bulunan adres listedekinden farklıydı.
- Listedeki adres güvenilir bir "doğru cevap" değil. Üç şirkette daha eskimiş çıktı: BK Mobil (`bkmobil.com.tr`, `bktomorrow.com`'a yönleniyor), İLG (`ilg.com.tr` açılmıyor, şirket `ilgtechnologies.com`'da ve sayfasında "Development Office Bilkent Cyberpark" yazıyor), A2 (`a2labs.com.tr` sertifika hatası veriyor). Önceki denemelerdeki "bulunamadı" sayıları bu yüzden olduğundan kötü görünüyor olabilir.
- Doğrulama kuralında delik: A2 için seçilen `a2technology.co` sitesi "Ankara" kelimesiyle doğrulandı, ama kelime müşteri listesinde geçiyordu ("Ankara Emniyet Müdürlüğü"). Şirket adı uyuyor ("a2 Teknoloji"), büyük ihtimalle doğru şirket; ama doğrulama yanlış sebeple geçti.
- E-A Teknoloji: doğru site ilk sıradaydı, sayfada şehir adı geçmediği için doğrulanamadı.
- İki şirket hiçbir yöntemle bulunamadı: C.B.K. Soft, CE Tasarım (sitesi `positive.com.tr`, alan adında şirket adı yok).

## 16. Site bulma, deneme 8: iki adımlı arama ve sıkı doğrulama (2026-11-13)

Yöntem: (1) sadece adla ara, ilk 5 sonuç; (2) kabul edilen site yoksa ad + "Ankara" ile ara, ilk 10 sonuç; (3) sıkı doğrulama: sayfada "Cyberpark" ya da "Bilkent" geçmeli, ya da "Ankara" bir adresin içinde olmalı (yakınında posta kodu, Çankaya, mahalle, cadde, teknokent). "Ankara" tek başınaysa site kabul edilmez. Daha önce hiçbir site bulma denemesinde kullanılmamış şirketler; ilk kelimesi kısa olanlar adresi bilinen grupta yok. Betik: `trials/trial_two_step.py`.

Adresi bilinen 10 şirket (seed 20261122):

| Kriter | Sonuç |
|---|---|
| Kabul edilen doğru site: en az 7/10 | Tutmadı: 6/10 |
| Kabul edilen yanlış site: 0 | Tuttu: 0 |
| Sıkı doğrulamanın elediği doğru site: en fazla 1 | Tuttu: 0 (ama "Ankara" tek başına geçen site hiç çıkmadı, kural zorlanmadı) |

Kabul edilmeyen 4 şirket:
- Solveka: doğru site seçildi, ama site sadece `http` ile açılıyor ve doğrulama adımı sadece `https` deniyordu. Betikteki hata düzeltildi; düzeltmeden sonra site doğrulandı. Kriter sonucu 6/10 kalır, düzeltmeyle 7/10.
- Argem: doğru site ilk sıradaydı, ama sitede şehir ya da teknokent adı hiç geçmiyor.
- Sistematik İnovasyon: sitesi `innocentrum.com`, alan adında şirket adı yok. İkinci sorguda 4. sıradaydı ama kural seçemedi.
- OneZero: sitesi (`onezeroi.com`) iki sorguda da sonuçlara girmedi.

İkinci sorgu 1 şirket kazandırdı (Rocksoft: sadece adla sonuçlarda yoktu, "Ankara" ile 4. sırada geldi).

Adresi olmayan 10 şirket (seed 20261123):

| Sonuç | Sayı | Şirketler |
|---|---|---|
| Kabul edildi | 8 | Zihinler Fora, RunX, Swart, Oasis, Clonify Labs, Cognito, Pulsetronics, Poetas |
| Seçildi ama okunamadı | 1 | Berca (site sadece `http` ile açılıyor; hata düzeltildikten sonra doğrulandı) |
| Bulunamadı | 1 | Kozkarlar |

- Kabul edilen 8 sitenin 7'sinde sayfada "Cyberpark" ya da "Bilkent" yazıyor, alan adı da şirket adını taşıyor. Sekizincisi (Oasis) adres içindeki "Ankara" ile doğrulandı; site başlığı "Oasis Teknoloji | Enerji ve Yapay Zeka Çözümleri", şirketin unvanıyla uyuşuyor.
- Yanlış site kabul edilmedi. Berca için ilk sorguda Endonezya'daki bir şirketin sitesi seçildi, doğrulama eledi.
- Önceki denemelerde adresi olmayan şirketlerde 10'da 3 kabul ediliyordu. Fark kısmen yöntemden (Playwright'lı doğrulama, ikinci sorgu), kısmen örneklemden geliyor olabilir; ayrıştırılmadı.

Site bulma denemelerinin toplamı (bölüm 7-16): yaklaşık 150 Tavily kredisi. Doğrulama adımı eklendikten sonraki dört denemede kesin yanlış olduğu görülen hiçbir site kabul edilmedi.

## 17. Site scan, deneme 9: sayfaları seçme ve okuma (2026-11-13)

Sitesi daha önce okunmamış, adresi yazan rastgele 15 şirket (seed 20261124). Her ana sayfa hem düz okundu hem Playwright ile açıldı. Sayfa seçimi: ana sayfadaki bağlantılar metnine ve adresine göre puanlandı, haber ve blog adresleri dışlandı, en fazla 2 ürün ya da hizmet, 1 hakkımızda, 1 kariyer sayfası seçildi. Betikler: `trials/sitescan.py`, `trials/trial_site_scan.py`.

| Kriter | Sonuç |
|---|---|
| "Düz okuma 50 kelimenin altındaysa Playwright" kuralı, içeriği JavaScript ile gelen siteleri kaçırmamalı | Tuttu: 3 siteden 3'ünü yakaladı |
| Kural en fazla 2 sitede gereksiz yere Playwright açtırmalı | Tuttu: 1 (A2, site hiç açılmıyor) |
| Seçilen ürün sayfası, ayrı ürün sayfası olan sitelerin en az %80'inde gerçekten ürün ya da hizmet sayfası olmalı | Tuttu: 10/12 (%83) |

- Düz okumada ana sayfa kelime sayıları iki kümeye ayrıldı: JavaScript ile yüklenen sitelerde 0, 0, 3; diğerlerinde en az 193. 50 kelimelik eşik bu boşluğun içinde.
- 15 sitenin 3'ü (%20) JavaScript ile yükleniyor: BNCool, Konumsal, Zeg. Üçü de Playwright ile okundu.
- Paydaya girmeyen 3 site: A2 (açılmıyor), UMRAM (araştırma merkezi, ürün sayfası yok), Mora (tek sayfalık site, menü bağlantıları sayfa içi; içerik zaten ana sayfada).
- Yanlış çıkan 2 site:
  - Birfatura: "Projesoft entegrasyonu" sayfası ("proje" kelimesi eşleşti) ve bir blog yazısı ("Etsy'de en çok satılan ürünler") seçildi.
  - T2: hizmet sayfasının adı "Consulting", kelime listesinde yoktu.
- Görülen diğer kusurlar: aynı sayfa `www`'li ve `www`'suz iki kez seçildi (innoCentrum); "Kariyer" bağlantısı hakkımızda sayfasının bir bölümüne gidiyordu ve hakkımızda sayfası kariyer diye seçildi (T2); innoCentrum'da asıl ürün "Platform" ve "Modüller" altında, "Hizmetler" seçildi.
- Her sayfanın metni menüyle başlıyor ve menü her sayfada tekrar ediyor. Oska'da seçilen üç sayfanın ilk 75 kelimesi aynı. Groq'a gönderilen metnin önemli bir kısmı tekrar.

## 18. Groq'a gidecek metni temizleme, deneme 10 (2026-11-13)

Deneme 9'daki 15 sitenin seçilen sayfalarında üç yöntem: ham metin, trafilatura 2.3.1 (varsayılan ve `favor_recall`), tekrar eden satırı atma (bir satır sitenin sayfalarında ilk geçtiği yerde kalır, tekrarları silinir). Ölçü: ham metindeki en az 12 kelimelik satırlar "içerik cümlesi" sayıldı. Betik: `trials/trial_text_cleaning.py`. Açılmayan A2 hesaba katılmadı (14 site).

| Kriter | Tekrar eden satırı atma | Trafilatura | Trafilatura, favor_recall |
|---|---|---|---|
| Metin ortancada en az %30 kısalmalı | Tutmadı: %28 | Tuttu: %52 | Tuttu: %52 |
| İçerik cümlelerinin ortancada en az %90'ı korunmalı | %100 (aşağıdaki nota bakın) | Tutmadı: %76 | Tutmadı: %67 |
| En kötü sitede en az %50 korunmalı | %100 | Tutmadı: %0 | Tutmadı: %0 |

Hiçbir yöntem üç kriteri birden geçmedi. Ama ölçünün kendisi kusurlu çıktı:
- Tekrar eden satırı atma yöntemi tanımı gereği hiçbir farklı satırı silmez; %100 korunma bir ölçüm değil, yöntemin tanımı.
- "En az 12 kelimelik satır" çerez bildirimlerini, kullanıcı yorumlarını ve adres satırlarını da içerik sayıyor. Trafilatura'nın "kaybettiği" cümlelerin bir kısmı tam da atılması istenen şeyler: Oska'da çerez metinleri, Mora'da oyun yorumları.
- Trafilatura gerçek içerik de attı: Zeg'in hakkımızda sayfasındaki ekip ve süreç paragrafları, adres satırları.
- Mora'da ölçü %0 gösterdi, ama trafilatura çıktısı elle bakınca iyiydi: oyunların adları ve açıklamaları duruyor.

Ölçülebilen kesin şeyler:
- Tekrar eden satırı atmak risksiz ve metni yaklaşık dörtte bir kısaltıyor (en çok Oska %64, BNCool %59).
- Trafilatura metni yaklaşık yarıya indiriyor.
- Groq'un dakikalık sınırı yaklaşık 2.500 kelimeye izin veriyor. Ham metin 14 sitenin 5'inde bunu aşıyor, tekrar atılınca 2'sinde, trafilatura ile hiçbirinde.

Doğru ölçü cümle saymak değil, Groq'un cevabının değişip değişmediği. Sonraki deneme bunu ölçecek.

## 19. Metin temizlemenin Groq'un cevabına etkisi, deneme 11 (2026-11-14)

Deneme 9-10'daki 14 sitenin kayıtlı sayfaları üç metinle soruldu: ham, tekrarları atılmış, trafilatura. Her metin 2.300 kelimede kesildi. Soru metni deneme 2 ile aynı. Etiketler denemeden önce yazıldı: "kendi yazılımını geliştiriyor mu" 13 sitede (10 evet, 3 hayır), "üründe yapay zekâ" 11 sitede (2 evet); etiketi kesin olmayanlar sayılmadı. Betikler: `trials/groq_extract.py`, `trials/trial_groq_text_variants.py`. 42 istek, yaklaşık 45 dakika.

| Kriter | Sonuç |
|---|---|
| Tekrar atma yönteminin doğru cevap sayısı hamınkinden düşük olmamalı | Tuttu: ikisi de 22/24 |
| Trafilatura'nın doğru cevap sayısı tekrar atma yönteminden düşük olmamalı | Tuttu: 22/24 |
| Her yöntemde kanıt cümlelerinin hepsi gönderilen metinde geçmeli | Tutmadı: ham 28/31, tekrar atma 27/31, trafilatura 29/32 |

| Yöntem | Kendi yazılımı | Yapay zekâ | Kanıt bulundu | Giriş token toplamı |
|---|---|---|---|---|
| Ham | 11/13 | 11/11 | 28/31 | 56.567 |
| Tekrarları atılmış | 11/13 | 11/11 | 27/31 | 45.369 (-%20) |
| Trafilatura | 12/13 | 10/11 | 29/32 | 36.428 (-%36) |

- Doğruluk açısından üç yöntem arasında fark yok. Trafilatura bir cevap kazandı (UMRAM: ham metinde "MRI Software and AI" başlığı yüzünden "evet" denmişti), bir cevap kaybetti (Pleksus: ana sayfadaki yapay zekâ cümlesini attığı için "bilinmiyor").
- Kanıt cümlelerinin yaklaşık %11'i bulunamadı (94'te 10). Önceki denemelerde bu oran %4'tü (47'de 2). Bulunamayan 10 kanıtın 5'inde model uzun cümleyi "..." ile kısaltmış. Diğerlerinde ayrı satırları birleştirmiş ya da ürün adlarını liste halinde yazmış. 25 kelime sınırı modeli uzun cümleyi kısaltmaya itiyor olabilir; sınanmadı.
- Kanıt kontrolü kuralı uygulanınca kabul edilen doğru "kendi yazılımı" cevabı: ham 9, tekrar atma 8, trafilatura 10.
- T2'de model üç metinde de kendisiyle çelişti: özetinde "yazılım geliştirme hizmeti sunan bir şirket" dedi, kanıt olarak "On-demand software development" gösterdi, ama "kendi yazılımını geliştiriyor mu" sorusuna "hayır" dedi. Sorudaki "danışmanlık yazılım geliştirmek değildir" örneği, müşteriye yazılım geliştiren şirketi yanlış tarafa itiyor olabilir.
- Etiketi kesin olmayan Zeo'da üç metin üç farklı cevap verdi: bilinmiyor, hayır, evet. Belirsiz şirketlerde cevap, metnin hangi kısmının gönderildiğine bağlı.
- Yapay zekâ sorusunda "hayır" ve "bilinmiyor" cevapları aynı sitede metinden metine değişti. İkisi de doğru sayıldı; model bu ikisini tutarlı ayırmıyor.
- 13 şirketin 10'u "evet" olduğu için bu örneklem "hayır" cevabını zayıf sınıyor. Üç "hayır" şirketinden ikisi (BNCool, Antenom) üç metinde de doğru çıktı.
