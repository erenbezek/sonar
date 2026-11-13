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
