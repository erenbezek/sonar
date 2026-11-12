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
