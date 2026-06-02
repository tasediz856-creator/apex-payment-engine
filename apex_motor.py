

import asyncio
import hmac
import hashlib
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# FastAPI Uygulaması
app = FastAPI(title="APEX Async Ödeme Motoru API")
SECRET_KEY = b"apex_super_secret_key_987654321"

# İnternetten gelecek kart verilerinin kalıbı
class Odemetalebi(BaseModel):
    kart_sahibi: str
    kart_no: str
    son_kullanma_tarihi: str
    cvv: str
    tutar: float
    siparis_id: str

# Asenkron Ödeme Çekirdeği
async def apex_motoru_calistir(talep: Odemetalebi):
    veri_katmani = f"{talep.kart_no}-{talep.tutar}-{talep.siparis_id}".encode()
    dijital_imza = hmac.new(SECRET_KEY, veri_katmani, hashlib.sha256).hexdigest()
    await asyncio.sleep(0.1)  # 100ms banka onay süresi simülasyonu
    
    return {
        "durum": "SUCCESS",
        "mesaj": "Ödeme başarıyla tahsil edildi.",
        "islem_id": f"APX-{int(time.time())}-{talep.siparis_id}",
        "dijital_imza": dijital_imza,
        "islem_zamani": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    }

# Dış dünyaya açılan kapı (API Endpoint)
@app.post("/api/v1/pay")
async def odeme_noktasi(talep: Odemetalebi):
    if len(talep.kart_no) < 16 or len(talep.cvv) < 3:
        raise HTTPException(status_code=400, detail="Geçersiz kart veya CVV bilgisi!")
    if talep.tutar <= 0:
        raise HTTPException(status_code=400, detail="Ödeme tutarı 0'dan büyük olmalıdır!")
    try:
        sonuc = await apex_motoru_calistir(talep)
        return sonuc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sistemsel Hata: {str(e)}")

# Render'ın çalıştıracağı port ayarı (10000)
if __name__ == "__main__":
    uvicorn.run("apex_motor:app", host="0.0.0.0", port=10000, reload=True)
