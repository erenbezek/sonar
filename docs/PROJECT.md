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

Henüz uygulama kodu yok. Access check yapıldı ve geçti (2026-11-12).

Access check sonucu (kriter sonuçtan önce yazılmıştı):
- Aşama 1'in üç kaynağı (Cyberpark, ODTÜ, Hacettepe) GitHub Actions'tan 3 çalışmanın 3'ünde de açıldı.
- Yerelde açılan 9 örnek şirket sitesinin 9'u Actions'tan da açıldı.
- OSTİM ve SASAD da Actions'tan açıldı.
- Bakanlık TGB listesi Actions'tan açılmadı (bağlantı kurulamadı). Etkisi küçük: içeriği 14 teknokentin sabit listesi.
- OSSA kararsız: sunucusu bazen 3 saniyede tam yanıt veriyor, bazen indirmenin ortasında takılıyor. Bu hem yerelde hem Actions'ta oluyor, yani Actions'a özgü değil. Aşama 3'te tekrar deneme ve uzun bekleme süresi gerekecek.

Access check'te çıkan bulgular:
- Cyberpark ve Meteksan sertifika zincirini eksik gönderiyor. Eksik ara sertifika `certs/` klasörüne eklendi. İki site de doğrulama açıkken hem yerelde hem Actions'ta açılıyor.
- Bir site yerelde açılıp Actions'ta açılmayabiliyor, tersi de oluyor. Yerelde açılması tek başına kanıt değil.
- Sunucu 200 dönse bile sayfa yarım ya da boş gelebiliyor. Bunu sadece sayfada beklenen metni aramak yakalıyor.

Puan yapısı karara bağlandı (2026-11-12):
- Puan hiçbir şirketi elemez. Tek eleme, şirketin yazılım işi yapmadığına dair kanıt.
- İki kuyruk var: apply queue (açık ilanı olanlar) ve outreach queue (ilanı olmayan ama uygun görünenler). Card'lar ikisinden yarı yarıya gelir, kuyruk içindeki sırayı fit score belirler.
- Her 5 card'dan 1'i explore card.
- Bilgi bulunamayan şirket düşük puan almaz, low data olarak işaretlenir.
- Remote ya da hibrit çalışma artı puan getirir, ofiste çalışma eksi getirmez.
- ASELSAN, HAVELSAN ve Roketsan card olarak gönderilmez.

Henüz karara bağlanmamış konular: fit score'un parçaları ve ağırlıkları, test setinin hazırlanışı (seçim, etiketleme yeri, kaçırma kriterinin rakamı), trafilatura kütüphanesi, botun çalışma sıklığı.

Aşama 1 kapsamı: Cyberpark, ODTÜ ve Hacettepe adapter'ları, birleştirme, basit puan, Neon, bot ve haftalık özet.
