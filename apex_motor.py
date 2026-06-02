from decimal import Decimal, getcontext
import queue
import time
import uuid

# =====================================================================
# 1. KATMAN: FİNANSAL KESİNLİK AYARI (ACID PRENSİPLERİ)
# =====================================================================
# Bankacılık standartlarında yuvarlama hatasını sıfıra indirmek için
# float yerine 28 basamak kesinlikli Decimal yapısını kuruyoruz.
getcontext().prec = 28

# Gerçek dünyada PostgreSQL veritabanında tutulacak bakiye havuzumuz
VERITABANI_BAKIYELERI = {
    "SIRKET_A_TRENDYOL": Decimal("5000000000.00"),  # 5 Milyar TL bakiye
    "SIRKET_B_GETIR": Decimal("100000000.00"),
    "BIZIM_KASA_KOMISYON": Decimal("0.00")  # Günde 5 Milyon TL birikecek kasa
}

# =====================================================================
# 2. KATMAN: ŞOK EMİCİ KUYRUK (APACHE KAFKA MANTIĞI)
# =====================================================================
# Milyonlarca insan aynı anda "Ödeme Yap" dediğinde sistem çökmesin diye
# gelen tüm talepleri bu dijital bekleme salonuna (kuyruğa) alıyoruz.
islem_kuyrugu = queue.Queue()

def internetten_istek_yakala(gonderen_id, alan_id, miktar_str):
    """Müşteriler web sitesinden butona bastığı an tetiklenen fonksiyon.
    Sistemi yormaz, isteği kapıp hemen kuyruğa fırlatır."""
    istek_id = str(uuid.uuid4())
    istek_paketi = {
        "istek_id": istek_id,
        "gonderen": gonderen_id,
        "alan": alan_id,
        "miktar": Decimal(miktar_str)
    }
    islem_kuyrugu.put(istek_paketi)
    print(f"📥 [İstek Geldi] -> Kuyruğa Alındı. ID: {istek_id[:8]}... | Miktar: {miktar_str} TL")

# =====================================================================
# 3. KATMAN: MİLYARLIK İŞLEM MOTORU (CORE ENGINE)
# =====================================================================
def milyarlik_islem_motorunu_tetikle():
    """Sunucuda 7/24 çalışacak dev beyin. Kuyruğa giren tüm istekleri
    sırayla, mikrosaniyeler içinde ve sıfır riskle işler."""
    print("\n🚀 [MİLYARLIK MOTOR BAŞLATILDI] Kuyruktaki işlemler eritiliyor...\n")
    print("-" * 60)
    
    while not islem_kuyrugu.empty():
        # Kuyruğun en önündeki işlemi çek al
        istek = islem_kuyrugu.get()
        
        gonderen = istek["gonderen"]
        alan = istek["alan"]
        miktar = istek["miktar"]
        
        # Bakiye kontrolü (Güvenlik Duvarı)
        if VERITABANI_BAKIYELERI[gonderen] >= miktar:
            
            # GÜNDE 5 MİLYON TL KAZANDIRAN FORMÜL: %0.5 (Binde 5) Komisyon
            komisyon = miktar * Decimal("0.005")
            net_aktarilan = miktar - komisyon
            
            # HESAPLAR ARASI TRANSFER (Atomik İşlem: Biri düşerken diğeri artar)
            VERITABANI_BAKIYELERI[gonderen] -= miktar
            VERITABANI_BAKIYELERI[alan] += net_aktarilan
            
            # BİZİM CEBE GİREN PARA
            VERITABANI_BAKIYELERI["BIZIM_KASA_KOMISYON"] += komisyon
            
            print(f"✅ İŞLEM ONAYLANDI | ID: {istek['istek_id'][:8]}...")
            print(f"   💸 {gonderen} hesabından {miktar:,.2f} TL çıktı.")
            print(f"   💰 BİZİM KAZANÇ (Komisyon): +{komisyon:,.2f} TL")
        else:
            print(f"❌ İŞLEM REDDEDİLDİ | ID: {istek['istek_id'][:8]}... -> Yetersiz Bakiye!")
            
        print("-" * 60)
        islem_kuyrugu.task_done()

# =====================================================================
# 4. KATMAN: CANLI SİMÜLASYON VE TETİKLEME
# =====================================================================
if __name__ == "__main__":
    print("=== APEX ÖDEME TEKNOLOJİLERİ SİSTEMİ BAŞLADI ===\n")
    
    # Senaryo: Büyük şirketler aynı saniyede bizim sistemimize istek gönderiyor
    internetten_istek_yakala("SIRKET_A_TRENDYOL", "SIRKET_B_GETIR", "1000000000.00") # 1 Milyar TL
    internetten_istek_yakala("SIRKET_A_TRENDYOL", "SIRKET_B_GETIR", "500000000.00")  # 500 Milyon TL
    internetten_istek_yakala("SIRKET_A_TRENDYOL", "SIRKET_B_GETIR", "200000000.00")  # 200 Milyon TL
    
    # Motoru çalıştırıp kuyruktaki paraları eritiyoruz
    milyarlik_islem_motorunu_tetikle()
    
    # Gün sonu raporu: Bizim şirketin net kasası
    print("\n================== GÜN SONU KASA RAPORU ==================")
    print(f"📈 Şirketimizin Bugün Kazandığı Net Komisyon: {VERITABANI_BAKIYELERI['BIZIM_KASA_KOMISYON']:,.2f} TL")
    print("==========================================================")
