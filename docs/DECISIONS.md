# DECISIONS

| Tarih | Karar | Neden |
|---|---|---|
| 2026-10-21 | Dil: Python | En olgun ekosistem onda: sayfa okuma, PDF ayrıştırma ve JavaScript ile yüklenen sayfaları açma. |
| 2026-10-21 | Veritabanı: PostgreSQL, Neon ücretsiz katman | Ücretsiz ve kullanılmadığında sıfıra iniyor. Supabase 7 gün işlem olmazsa veritabanını duraklatıyor. |
| 2026-10-21 | VM yok. Toplama, zenginleştirme ve bot GitHub Actions'ta zamanlanmış çalışır. | Ücretsiz VM'ler kart doğrulaması istiyor, Oracle boşta kalan sunucuyu geri alabiliyor. Bedeli: butonlar anında işlenmez, bir sonraki çalışmada işlenir. Telegram basışları 24 saat saklar. |
| 2026-10-21 | Repo public | Actions dakikası sınırsız. Loglarda şirket adı görünmesi sorun değil (Eren). Bedeli: 60 gün commit olmazsa GitHub zamanlanmış işleri kapatır. |
| 2026-10-21 | Anahtarlar (Telegram, Neon, Gemini) GitHub Secrets'ta durur, repoya girmez. | Repo public. |
| 2026-10-21 | Yapay zekâ: Google AI Studio (Gemini API ücretsiz katman), isteğe bağlı | Ücretsiz. Kota günde ~100 istek, bu yüzden sadece en yüksek puanlı adaylarda kullanılır ve sonuç saklanır. Ücretsiz katmanda veri Google'ın ürün geliştirmesinde kullanılabildiği için sadece herkese açık şirket verisi gönderilir. |
| 2026-10-21 | Haftalık sabit sayı yok. Sıralı kuyruk, en yüksek puanlı N şirket gönderilir. | Optimum N = haftada işlenebilen şirket sayısı ÷ seçilme oranı. Değer ölçülecek. |
| 2026-10-21 | Kişi bulma ve mesaj manuel kalır. | LinkedIn kazımada hesap kapanması ve KVKK riski var. |
| 2026-11-12 | Hedef: staj sonrası iş. | Eren'in kararı. |
| 2026-11-12 | Büyük şirket olmak eksi puan getirmez. | Eren'in kararı. |
| 2026-11-12 | Tek puan yerine iki ayrı puan: fit score ve timing score. Toplanmazlar. | "İster miyim" ile "şimdi alır mı" ayrı sorular. Tek puan ikisini karıştırıyordu. |
| 2026-11-12 | Canlıya çıkmadan önce 40-50 şirketlik bir test seti elle etiketlenecek. | Puanlamanın işe yarayıp yaramadığını haftalar beklemeden ölçmek için. |
| 2026-11-12 | Şirkete özel araştırma için bir web arama servisi eklenecek. Sağlayıcı henüz seçilmedi. | Şirketin kendi sitesi haber ve ilan bulmak için yetmiyor. |
| 2026-11-12 | Dosya, kod ve terim isimleri İngilizce. Açıklamalar Türkçe. | Eren'in kararı. |
| 2026-11-12 | Uygulama kodundan önce access check yapılır. | Kaynaklar yalnızca yerelden doğrulanmıştı. Actions'ın çıkış adresleri engelleniyorsa "VM yok" kararı etkilenir. |
| 2026-11-12 | Access check geçti. "VM yok, her şey GitHub Actions'ta" kararı geçerli kalıyor. | Aşama 1'in üç kaynağı Actions'tan 3/3 açıldı, yerelde açılan 9 şirket sitesinin 9'u açıldı. Açılmayanlar: Bakanlık TGB listesi ve OSSA. |
| 2026-11-12 | Sertifika zincirini eksik gönderen siteler için eksik ara sertifika kendi güven listemize eklenir. Sertifika doğrulaması kapatılmaz. | Doğrulama kapatılırsa araya giren biri sahte veri gösterebilir. Cyberpark ve Meteksan'ın ikisi de aynı ara sertifikayı kullanıyor: Sectigo Public Server Authentication CA DV R36 (2036'ya kadar geçerli). Yerelde curl ve Python ile denendi, doğrulama açıkken iki site de açıldı. |
| 2026-11-12 | Düzeltme: OSSA'nın açılmaması Actions'a özgü değil. | Sonraki çalışmalarda OSSA Actions'tan tam indi, yerelde yarım indi. Sunucusu kararsız: aynı istek bazen 3 saniyede bitiyor, bazen 90 saniyede bile bitmiyor. Actions'tan açılmayan tek kaynak Bakanlık TGB listesi. |
| 2026-11-12 | Ara sertifika kararı uygulandı: `certs/sectigo-dv-r36.pem` eklendi, access check artık doğrulamayı hiç kapatmıyor. | Cyberpark ve Meteksan doğrulama açıkken yerelde ve Actions'ta açıldı. |
| 2026-11-12 | Yapay zekâ iş bölümü: toplu iş (sitelerden olgu çıkarma) Groq'ta, şirkete özel derin rapor Gemini'de. Her iş tek ve sabit modelde yapılır. | Groq'un günlük istek kotası yüksek, Gemini tek seferde uzun metin okuyabiliyor. Aynı iş farklı modellere dağılırsa aynı şirket farklı günlerde farklı olgular alır. |
| 2026-11-12 | Web arama servisi: Tavily. | Ücretsiz katmanı kart istemiyor (ayda ~1.000 kredi), sayfanın temiz metnini ve alaka puanını veriyor. |
| 2026-11-12 | Aşama 1 kütüphaneleri: httpx, beautifulsoup4 + lxml, psycopg 3 (düz SQL), rapidfuzz. Geliştirme: pytest, ruff. Paket yönetimi: uv. Telegram ve Tavily ayrı paket olmadan httpx ile çağrılır. Ayar dosyası için Python'un kendi tomllib'i kullanılır. | Az bağımlılık. Bot sürekli açık bir program olmadığı için büyük bot kütüphanesine gerek yok. |
| 2026-11-12 | Sonraki aşamalar için: Groq ve Gemini openai paketiyle çağrılır, PDF için pypdf. JavaScript ile yüklenen sayfalarda önce verinin geldiği adres aranır, olmazsa Playwright. | İki yapay zekâ sağlayıcısı da aynı tip arayüz sunuyor, tek paket yetiyor. |
| 2026-11-12 | Puan hiçbir şirketi elemez, yalnızca sırayı belirler. Listeden çıkarmanın tek yolu, şirketin yazılım işi yapmadığına dair kanıt. Her şirket veritabanında kalır ve adıyla sorulabilir. | İlan açmayan ama uygun şirketler de alım yapabiliyor, oradaki çalışanlara ulaşmak bir yol (Eren). Yanlış öneri ucuz ("Geç", 10 saniye), kaçırılan şirket pahalı. |
| 2026-11-12 | Timing score sıralamaz, kuyruğu seçer. İki kuyruk var: apply queue (açık ilanı olanlar) ve outreach queue (ilanı olmayan ama uygun görünenler). Card'lar iki kuyruktan yarı yarıya gelir. Kuyruk içindeki sırayı fit score belirler. | İlan sıralamayı belirlerse ilanı olmayan şirketlere sıra gelmez. Yarı yarıya oran başlangıç değeri: kuyruk başına cevap oranı ölçülecek. |
| 2026-11-12 | Yukarıdaki iki karar, 2026-10-21 tarihli "sıralı kuyruk, en yüksek puanlı N şirket gönderilir" kararının yerini alır. | Tek sıralı kuyruk ilanı olmayan şirketleri sona itiyordu. |
| 2026-11-12 | Her 5 card'dan 1'i explore card: düşük puanlı ya da low data işaretli şirketlerden rastgele seçilir. | Puanın aşağı ittiği şirketleri görmenin tek yolu. Explore card'lar üst sıradakiler kadar sık "İlgileniyorum" alıyorsa puan işe yaramıyor demektir. |
| 2026-11-12 | Bilgi bulunamaması düşük puan getirmez. Şirket low data olarak işaretlenir. | "Bilinmiyor" ile "yok" aynı şey değil. Küçük ama iyi bir şirketin sitesi zayıf olabilir. |
| 2026-11-12 | Remote ya da hibrit çalışma bulunursa fit score'a artı puan gelir. Ofiste çalışma ya da bilgi yokluğu eksi getirmez. Bulunan bilgi card'da gösterilir. | Eren'in kararı. |
| 2026-11-12 | ASELSAN, HAVELSAN ve Roketsan card olarak gönderilmez. | Eren'in kararı. |
