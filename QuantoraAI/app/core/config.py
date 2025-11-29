# LLM ayarları, sabit değişkenler ve konfigürasyonlar.

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# .env dosyasını yükle
load_dotenv()

# --- SABİT DEĞİŞKENLER ---
PROJECT_NAME = "QuantoraAI"
VERSION = "1.0.0 (Alpha)"

# --- MODEL AYARLARI ---
# Gemini 2.0 Flash: Hız ve geniş context için
MODEL_NAME = "gemini-2.0-flash" 

# API Anahtarı Kontrolü
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("HATA: .env dosyasında GEMINI_API_KEY bulunamadı!")

# --- MODEL NESNESİ (Singleton) ---
# Bu fonksiyonu tüm ajanlar ortak kullanacak.
def get_llm(temperature=0.3):
    return ChatGoogleGenerativeAI(
        model=MODEL_NAME,
        google_api_key=GOOGLE_API_KEY,
        temperature=temperature,
        convert_system_message_to_human=True
    )