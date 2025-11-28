from langchain.tools import tool
import requests
import os
from dotenv import load_dotenv

# .env dosyasındaki gizli değişkenleri (API anahtarı gibi) sisteme yükler.
load_dotenv()

# @tool dekoratörü: Bu fonksiyonu LangChain'in anlayabileceği bir "araç" (tool) haline getirir.
# Bu sayede bir AI ajanı (Agent), gerektiğinde bu fonksiyonu kendisi çağırabilir.
@tool
def get_stock_info(ticker: str) -> str:
    """
    Bir hisse senedi sembolü (örn: AAPL, GOOGL) için
    Finnhub API üzerinden güncel fiyat bilgilerini döner.
    """
    try:
        # 1. Adım: Ortam değişkenlerinden (environment variables) API anahtarını al.
        api_key = os.getenv("FINNHUB_API_KEY")
        
        # Eğer anahtar bulunamazsa işlemi durdur ve uyarı ver.
        if not api_key:
            return "Finnhub API anahtarı bulunamadı. Lütfen .env dosyasını kontrol edin."

        # ticker: Hisse sembolü (örn: AAPL), token: API anahtarı
        url = f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={api_key}" # 2. Adım: API isteği için URL'i oluştur.

        
        # 3. Adım: Belirtilen URL'e bir HTTP GET isteği gönder.
        response = requests.get(url)

        # Eğer sunucudan başarılı (200 OK) yanıt gelmezse hata kodunu dön.
        if response.status_code != 200:
            return f"Hata: {response.status_code}"

        # 4. Adım: Gelen yanıtı JSON formatından Python sözlüğüne (dictionary) çevir.
        data = response.json()

        # 5. Adım: Sözlük içinden gerekli verileri çek ve formatlı bir metin oluştur.                
      
        return (
            f"{ticker} hisse bilgileri:\n" # Finnhub API kısaltmaları:
            f"Güncel Fiyat: {data.get('c')}\n" # c: Current price (Güncel fiyat)
            f"Açılış Fiyatı: {data.get('o')}\n"  # o: Open price (Açılış fiyatı)
            f"En Yüksek: {data.get('h')}\n"  # h: High price (Günün en yükseği)
            f"En Düşük: {data.get('l')}"   # l: Low price (Günün en düşüğü)
        )
    except Exception as e:
        return f"Beklenmeyen hata: {e}"  # Kod çalışırken beklenmeyen bir hata (internet kopması vb.) olursa burada yakala.

 
if __name__ == "__main__": # Bu blok, dosya doğrudan çalıştırıldığında devreye girer (import edildiğinde çalışmaz).
    # Tool'u test etmek için manuel olarak bir sembol gönderiyoruz.
    # LangChain tool'ları genellikle .run() metodu ile test edilir.
    print(get_stock_info.run({"ticker": "AAPL"}))