from decimal import Decimal, getcontext
import queue
import hmac
import hashlib
import uuid

# =====================================================================
# 1. KATMAN: FİNANSAL KESİNLİK AYARI (ACID PRENSİPLERİ)
# =====================================================================
getcontext().prec = 28

# Güvenli sistem mimarisi için gizli şifreleme anahtarı
SISTEM_GIZLI_ANAHTARI = b"apex_super_secret_key_2026"

VERITABANI_BAKIYELERI = {
    "SIRKET_A_TRENDYOL": Decimal("5000000000.00"),  # 5 Milyar TL bakiye
    "SIRKET_B_GETIR": Decimal("100000000.00"),
    "BIZIM_KASA_KOMISYON": Decimal("0.00")
}

islem_kuyrugu = queue.Queue()

# =====================================================================
# 2. KATMAN: SİBER GÜVENLİK (HMAC DIJITAL IMZA DOĞRULAMA)
# =====================================================================
def dijital_imza_olustur(gonderen, alan, miktar_str):
    """Verinin yolda değiştirilmediğini kanıtlayan siber imza oluşturur."""
    veri = f"{gonderen}-{alan}-{miktar_str}".encode()
    return hmac.new(SISTEM_GIZLI_ANAHTARI, veri, hashlib.sha256).hexdigest()

def internetten_istek_yakala(gonderen_id, alan_id, miktar_str, gelen_imza):
    istek_id = str(uuid.uuid4())
    
    # Güvenlik Kontrolü: İmza doğru mu?
    dogru_imza = dijital_imza_olustur(gonderen_id, alan_id, miktar_str)
    
    if not hmac.compare_digest(dogru_imza, gelen_imza):
        print(f"🚨 [SİBER SALDIRI ENGELLENDİ] Hatalı İmza! ID: {istek_id[:8]}... İstek çöpe atıldı.")
        return

    istek_paketi = {
        "istek_id": istek_id,
        "gonderen": gonderen_id,
        "alan": alan_id,
        "miktar": Decimal(miktar_str)
    }
    islem_kuyrugu.put(istek_paketi)
    print(f"📥 [İstek Güvenli] -> Kuyruğa Alındı. ID: {istek_id[:8]}... | Miktar: {miktar_str} TL")

# =====================================================================
# 3. KATMAN: MİLYARLIK İŞLEM MOTORU (CORE ENGINE)
# =====================================================================
def milyarlik_islem_motorunu_tetikle():
    print("\n🚀 [MİLYARLIK MOTOR BAŞLATILDI] Kuyruktaki işlemler eritiliyor...\n")
    print("-" * 60)
    
    while not islem_kuyrugu.empty():
        istek = islem_kuyrugu.get()
        gonderen = istek["gonderen"]
        alan = istek["alan"]
        miktar = istek["miktar"]
        
        if VERITABANI_BAKIYELERI[gonderen] >= miktar:
            komisyon = miktar * Decimal("0.005")
            net_aktarilan = miktar - komisyon
            
            VERITABANI_BAKIYELERI[gonderen] -= miktar
            VERITABANI_BAKIYELERI[alan] += net_aktarilan
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
    print("=== APEX GÜVENLİ ÖDEME SİSTEMİ BAŞLADI ===\n")
    
    # 1. Senaryo: Geçerli ve imzalı güvenli işlemler
    imza1 = dijital_imza_olustur("SIRKET_A_TRENDYOL", "SIRKET_B_GETIR", "1000000000.00")
    internetten_istek_yakala("SIRKET_A_TRENDYOL", "SIRKET_B_GETIR", "1000000000.00", imza1)
    
    # 2. Senaryo: Siber saldırı denemesi (Yolda veriyi değiştirip miktarı manipüle eden korsan)
    internetten_istek_yakala("SIRKET_A_TRENDYOL", "SIRKET_B_GETIR", "9999999999.00", "sahte_korsan_imzasi")
    
    milyarlik_islem_motorunu_tetikle()

