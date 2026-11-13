# GLOSSARY

İsimler İngilizce, açıklamalar Türkçe.

| İsim | Anlamı |
|---|---|
| sonar | Projenin adı. |
| card | Telegram'da tek bir şirketi anlatan mesaj. İlgileniyorum, Geç ve Sonra butonlarıyla gelir. |
| watchlist | "İlgileniyorum" denen şirketlerin listesi. Günlük değişiklik kontrolü bunlarda yapılır. |
| adapter | Tek bir kaynağı (ör. Cyberpark listesi) okuyup ortak biçime çeviren kod parçası. |
| growth signal | Şirketin sitesinde, ilanında ya da GitHub'ında Docker, Kubernetes, bulut, CI/CD veya üründe yapay zekâ geçmesi. |
| fit score | "Bu şirketi ister miyim?" sorusunun puanı. Şirketi elemez, kuyruk içindeki sırayı belirler. |
| timing score | "Bu şirket şimdi eleman alır mı?" sorusunun puanı. Açık ilan gibi sinyallerden gelir. Sıralamaz, şirketin hangi kuyruğa gireceğini belirler. |
| apply queue | Açık ilanı olan şirketlerin kuyruğu. Yol: ilana başvurmak. |
| outreach queue | İlanı olmayan ama uygun görünen şirketlerin kuyruğu. Yol: çalışanlardan birine ulaşmak. |
| explore card | Puandan bağımsız, rastgele seçilen card. Puanın kaçırdığı şirketleri görmek için gönderilir. |
| low data | Hakkında yeterli bilgi bulunamayan şirketin işareti. Düşük puan anlamına gelmez. |
| access check | Kaynak sitelere ve örnek şirket sitelerine birer istek atıp açılıp açılmadığını ölçen deneme. Hem yerelde hem GitHub Actions'ta çalışır. |
| certs | Bazı sitelerin göndermediği ara sertifikaların durduğu klasör. Sistem sertifikalarına eklenerek kullanılır. İlk dosya: `sectigo-dv-r36.pem`. |
| trials | Karar vermeden önce gerçek şirketlerde yapılan denemelerin betiklerinin durduğu klasör. Sonuçları `docs/FINDINGS.md`'ye yazılır. |
| site finder | Şirketin site adresini bulan adım. Adla arar, alan adına göre seçer, sayfadaki teknokent ya da adres bilgisiyle doğrular. |
| site scan | Şirketin sitesinden sayfaları okuyan adım. Okunan metin Groq'a verilir. |
