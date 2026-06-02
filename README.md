# 🚀 APEX: High-Speed Asynchronous Payment Engine

Büyük ölçekli e-ticaret pazar yerleri ve online oyun platformları için geliştirilmiş, yüksek yük altında kilitlenmeyen **Yeni Nesil FinTech Altyapı Motoru**.

---

## ⚡ Çözülen Problemler

* **Sistem Çökmeleri:** Geleneksel ödeme sistemleri saniyede binlerce anlık istek aldığında kilitlenir. APEX, araya koyduğu şok emici kuyruk mimarisiyle sistemi hafifletir.
* **Finansal Veri Kaybı:** Standart yazılımlardaki `float` veri tipi hatalı kuruş yuvarlamalarına sebep olur. APEX, bankacılık standartlarında kesinlik sunar.

---

## 🛠️ Öne Çıkan Teknolojik Özellikler

* **Asenkron Şok Emici Kuyruk (Queue):** Yoğun kampanya günlerinde gelen milyonlarca ödeme talebini sıraya dizerek sunucunun çökmesini engeller.
* **Finansal Kesinlik (Decimal):** Python `Decimal(28)` kesinlik modu kullanılarak kuruş yuvarlama hatası sıfıra indirilmiştir.
* **ACID Güvencesi:** İşlemler atomiktir. Sunucuda elektrik kesilse bile bakiye havada asılı kalmaz, sistem kendini korumaya alır.

---

## 📊 Canlı Simülasyon Çıktısı (Proof of Concept)

Sistem, tek bir salisede milyarlık transferleri sıfır hata ile eriterek günü kapatabilmektedir:

```text
=== APEX ÖDEME TEKNOLOJİLERİ SİSTEMİ BAŞLADI ===

📥 [İstek Geldi] -> Kuyruğa Alındı. | Miktar: 1,000,000,000.00 TL
📥 [İstek Geldi] -> Kuyruğa Alındı. | Miktar: 500,000,000.00 TL
📥 [İstek Geldi] -> Kuyruğa Alındı. | Miktar: 200,000,000.00 TL

🚀 [MİLYARLIK MOTOR BAŞLATILDI] Kuyruktaki işlemler eritiliyor...

✅ İŞLEM ONAYLANDI | 💸 TRENDYOL hesabından 1,000,000,000.00 TL çıktı. -> 💰 KOMİSYON: +5,000,000.00 TL
✅ İŞLEM ONAYLANDI | 💸 TRENDYOL hesabından 500,000,000.00 TL çıktı.   -> 💰 KOMİSYON: +2,500,000.00 TL
✅ İŞLEM ONAYLANDI | 💸 TRENDYOL hesabından 200,000,000.00 TL çıktı.   -> 💰 KOMİSYON: +1,000,000.00 TL

================== GÜN SONU KASA RAPORU ==================
📈 Şirketimizin Bugün Kazandığı Net Komisyon: 8,500,000.00 TL
==========================================================

