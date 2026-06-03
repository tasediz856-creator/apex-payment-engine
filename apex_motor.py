import uvicorn
import os
from fastapi import FastAPI, HTTPException

app = FastAPI()

# Railway için gerekli port ayarı
port = int(os.environ.get("PORT", 10000))

# --- BURAYA KENDİ MANTIKLARINI EKLEYEBİLİRSİN ---
# Örneğin veritabanı bağlantıları veya ödeme hesaplama fonksiyonların burada durabilir.

@app.get("/")
def read_root():
    return {"status": "Apex Payment Engine aktif", "version": "1.0.0"}

@app.post("/process-payment")
def process_payment(amount: float):
    # Ödeme motorunun çalıştığı yer
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Geçersiz ödeme tutarı")
    return {"message": f"{amount} TL tutarında ödeme işlendi", "status": "Success"}

# -----------------------------------------------

if __name__ == "__main__":
    # Railway ve benzeri bulut sistemleri için host 0.0.0.0 olmalıdır
    uvicorn.run("apex_motor:app", host="0.0.0.0", port=port)

