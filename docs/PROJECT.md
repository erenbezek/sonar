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

Henüz uygulama kodu yok. İlk iş olarak access check yapılıyor: kaynak sitelere GitHub Actions'tan erişilebiliyor mu?

Access check geçme kriteri (sonuçtan önce yazıldı):
- Aşama 1'in üç kaynağı (Cyberpark, ODTÜ, Hacettepe) 3 çalışmanın 3'ünde de açılmalı.
- Yerelde açılan örnek şirket sitelerinin en az %80'i Actions'tan da açılmalı.
- "Açıldı" demek: HTTP 200 dönmesi ve sayfada beklenen metnin bulunması.

Henüz karara bağlanmamış konular: puan ağırlıkları, kütüphaneler, yapay zekâ sağlayıcılarının iş bölümü, web arama servisinin sağlayıcısı, botun çalışma sıklığı.

Aşama 1 kapsamı: Cyberpark, ODTÜ ve Hacettepe adapter'ları, birleştirme, basit puan, Neon, bot ve haftalık özet.
