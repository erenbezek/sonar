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
