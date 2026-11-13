# PROJECT

## Ne

Sonar, Ankara'daki teknokent ve sektör listelerinden şirketleri toplayan, birleştiren ve puanlayan bir sistem. Öne çıkan şirketleri düzenli olarak Telegram'a card olarak gönderir. Her card'da üç buton olur: İlgileniyorum, Geç ve Sonra. "İlgileniyorum" denen şirketler watchlist'e girer. Bu şirketlerde yeni ilan gibi bir güncelleme olunca Telegram'a bildirim düşer. Başvuru ve temas takibi de Telegram üzerinden yapılır.

İsimlerin anlamı `GLOSSARY.md` dosyasında.

## Neden

Amaç, staj bittikten sonra junior backend olarak işe girme süresini kısaltmak.

- Hedef şirketler: teknokentlerdeki küçük ve orta ölçekli sivil yazılım şirketleri ve savunma alt yüklenicileri. İkisi eşit ağırlıkta.
- Öne çıkacak şirketler: backend ile başlayıp DevOps, AIOps ve AI engineering deneyimi kazanılabilecek yerler. Bunu growth signal gösterir.
- Şehir: Ankara, gerekirse İstanbul. Bursa'dan remote başlayıp mezuniyette ofise geçmek.
- Büyük şirketler ikincil. ASELSAN, HAVELSAN ve Roketsan hedef değil.

## Bitti sayılması için

- GitHub Actions'ta zamanlanmış olarak çalışıyor ve card'lar Telegram'a düşüyor.
- 4 hafta boyunca gönderilen card'ların en az %40'ı "İlgileniyorum" alıyor.
- Cevap oranı ve ilk temastan mülakata geçen gün sayısı ölçülüyor. Başlangıç değeri yok, ilk ölçüm referans olacak.

## Kapsam dışı

- Şirkette kişi bulma ve LinkedIn kazıma. Kişi bulma ve mesaj yazma manuel kalır.
- TÜBİTAK 2209-B.
- Ücretli servis ve VM.

## Şu an

Uygulama kodu henüz yok. Kararlar gerçek şirketlerde denenerek veriliyor: bulgular `FINDINGS.md`'de, deneme betikleri `trials/` klasöründe.

Karara bağlananlar (ayrıntı `DECISIONS.md`'de):
- Access check geçti (2026-11-12). Eksik ara sertifika `certs/` klasöründe.
- Puan hiçbir şirketi elemez. İki kuyruk var: apply queue ve outreach queue. Her 5 card'dan 1'i explore card. Bilgi bulunamayan şirket low data olur.
- Site adresi site finder ile bulunur (Tavily araması, alan adına göre seçim, sayfadaki adresle doğrulama).
- Site scan, Groq ve Playwright Aşama 1'de.
- Groq siteden kanıt cümlesiyle olgu çıkarır, kanıt kodla kontrol edilir.

Henüz karara bağlanmamış konular:
- Fit score'un parçaları. Önerilen tablo (backend 0/2, growth signal 0/1/2, remote 0/1) kelime eşleştirmeye dayanıyordu ve sitelerde çalışmadı. Groq'un çıkarabildiği olgulara göre yeniden ele alınacak.
- Groq'un "satıyor mu, geliştiriyor mu" ayrımı. Zor örnekte hâlâ yanılıyor.
- Site scan'in hangi sayfaları okuyacağı ve Playwright'a ne zaman başvuracağı.
- Listede adresi yazan şirketlerde adres eskimişse ne yapılacağı.
- Site finder'ın bulamadığı durumlar: alan adında şirket adı geçmeyenler, sitesinde adres yazmayanlar, ilk kelimesi kısa olanlar.
- Test setinin hazırlanışı, trafilatura kütüphanesi, botun çalışma sıklığı.

Aşama 1 kapsamı: Cyberpark, ODTÜ ve Hacettepe adapter'ları, site finder, site scan, Groq ile olgu çıkarma, birleştirme, basit puan, Neon, bot ve haftalık özet.
