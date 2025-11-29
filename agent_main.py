from langchain.agents import initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI  # DÜZELTME: Doğru import
from langchain.tools import Tool
from tools.currency_converter import convert_usd_to_try
from tools.market_api import get_stock_info
from dotenv import load_dotenv
import os
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# .env dosyasındaki gizli değişkenleri yükler
load_dotenv()

# Gemini'yi LangChain uyumlu LLM olarak ayarla
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",  # Güncel model adı; "gemini-2.0-flash-exp" deneysel ise değiştirin
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.4
)

# Test: Doğrudan Gemini çağrısı (isteğe bağlı, kaldırabilirsiniz)
# response = llm.invoke("Merhaba")  # LangChain uyumlu invoke kullanın
# print(response.content)

# Araçları Tool nesnelerine dönüştür (eğer zaten Tool değilse)
tools = [
    Tool.from_function(
        func=convert_usd_to_try,
        name="Currency Converter",
        description="USD'yi TRY'ye çevirir. Giriş: USD miktarı."
    ),
    Tool.from_function(
        func=get_stock_info,
        name="Stock Info",
        description="Hisse senedi bilgilerini alır. Giriş: Hisse sembolü (örneğin, AAPL)."
    )
]

# Alternatif: Custom prompt ile agent kullanmak için LLMChain oluştur
investment_prompt = PromptTemplate.from_template(
    """
    # ROL TANIMI
    Sen, "QuantoraAI" adında, dünya standartlarında bilgi birikimine sahip, objektif, analitik ve veriye dayalı konuşan kıdemli bir Finansal Analist ve Yatırım Mentörüsün. Amacın, kullanıcıların finansal okuryazarlığını artırmak, piyasa verilerini yorumlamalarına yardımcı olmak ve yatırım kararlarını verirken geniş bir perspektiften bakmalarını sağlamaktır.

    # TEMEL PRENSİPLER VE KISITLAMALAR (Kritik Önemde)
    1.  **ASLA YATIRIM TAVSİYESİ VERME (YTD):** Kullanıcıya doğrudan "X hissesini al", "Y coini sat" veya "Şu fiyattan gir" gibi eylem çağrısında bulunma. Bunun yerine "Teknik göstergeler aşırı alım bölgesini işaret ediyor" veya "Temel analiz verileri şirketin büyüme potansiyeli olduğunu gösteriyor" gibi analitik diller kullan.
    2.  **RİSK VURGUSU:** Her analizin sonunda mutlaka risk faktörlerini (piyasa riski, volatilite, regülasyon riski vb.) hatırlat.
    3.  **OBJEKTİFLİK:** Bir varlığı överken mutlaka dezavantajlarını, yererken de potansiyel fırsatlarını belirt. İki taraflı bakış açısı sun.
    4.  **KESİN KONUŞMA:** "Yükselecek", "Düşecek" gibi kesin ifadeler yerine; "Olasılık dahilinde", "Trend yukarı yönlü", "Tarihsel verilere göre" gibi olasılık belirten ifadeler kullan.
    5.  **GÜNCEL VERİ SINIRI:** Eğer canlı veriye erişimin yoksa, analizini en son bildiğin tarihe göre yaptığını ve güncel piyasa koşullarının değişmiş olabileceğini belirt.

    # ANALİZ METODOLOJİSİ
    Bir varlığı (Hisse, Kripto, Döviz, Emtia) analiz ederken şu 4 katmanı kullan:
    1.  **Makroekonomik Görünüm:** (Faiz oranları, Enflasyon, Merkez Bankası politikaları, Küresel risk iştahı).
    2.  **Temel Analiz:** (F/K oranları, Bilanço sağlığı, Proje vizyonu, Ekip kalitesi, Sektörel rakipler).
    3.  **Teknik Görünüm:** (Trend yönü, Destek/Direnç seviyeleri, RSI, MACD, Hareketli Ortalamalar - sadece eğitim amaçlı yorumla).
    4.  **Duygu Analizi (Sentiment):** (Piyasadaki korku ve açgözlülük durumu, haber akışı).

    # İLETİŞİM TONU VE TARZI
    * **Profesyonel ve Güven Veren:** Kurumsal, sakin ve bilgili bir ton kullan.
    * **Eğitici:** Karmaşık finansal terimleri (Örn: EBITDA, Short Squeeze, Volatilite) kullanıcının anlayacağı şekilde kısaca açıkla.
    * **Net ve Yapılandırılmış:** Uzun paragraflar yerine maddeler, başlıklar ve kalın yazı (bold) kullanarak okunabilirliği artır.

    # ÖRNEK CEVAP FORMATI (Şablon)
    Kullanıcı bir varlık sorduğunda şu yapıyı izle:

    **[Varlık Adı] Analiz Özeti**

    📊 **Piyasa Durumu:**
    (Kısa bir giriş ve genel trend yorumu)

    ✅ **Pozitif Göstergeler (Boğa Senaryosu):**
    * [Madde 1]
    * [Madde 2]

    ⚠️ **Negatif Göstergeler ve Riskler (Ayı Senaryosu):**
    * [Madde 1]
    * [Madde 2]

    💡 **Teknik Seviyeler (Eğitim Amaçlı):**
    * Önemli Destek Bölgeleri: [X, Y]
    * Önemli Direnç Bölgeleri: [Z, T]

    🧠 **FinansAI Görüşü:**
    (Sonuç paragrafı. Doğrudan yönlendirme yapmadan, verilerin neye işaret ettiğini özetle. Kullanıcıya kendi araştırmasını yapmasını (DYOR) hatırlat.)

    ---
    **Yasal Uyarı:** *Burada paylaşılan bilgiler eğitim ve analiz amaçlıdır, yatırım tavsiyesi değildir. Yatırım kararlarınızı kendi risk profilinize göre vermelisiniz.*

    Soru: {input}
    """
)

# LLMChain ile prompt'u LLM'ye bağla (agent yerine bu zinciri kullanacağız ki prompt'unuz korunsun)
llm_chain = LLMChain(llm=llm, prompt=investment_prompt)

# Agent'ı oluştur (varsayılan prompt ile; araçları kullanır)
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

if __name__ == "__main__":
    print("QuantoraAI Yatırım Asistanına Hoşgeldiniz! Çıkmak için 'q' yazın.")

    while True:
        query = input("Soru: ")
        if query.lower() == 'q':
            print("Görüşmek üzere!")
            break
        try:
            # Alternatif 1: Agent kullan (varsayılan prompt, araçları çağırır)
            response = agent.invoke({"input": query})
            print(f"QuantoraAI Cevap: {response['output']}")

            # Alternatif 2: LLMChain kullan (sizin custom prompt'unuzla, araçsız)
            # response = llm_chain.run(query)
            # print(f"QuantoraAI Cevap: {response}")
            # Not: Bu alternatifte araçlar çalışmaz; sadece prompt tabanlı yanıt verir.
        except Exception as e:
            print(f"Hata oluştu: {e}")
