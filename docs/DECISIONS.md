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
