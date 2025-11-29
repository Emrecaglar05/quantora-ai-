# Finansal Analist Ajanı (Node Mantığı).
from langchain_core.messages import SystemMessage, HumanMessage
from app.core.config import get_llm
from app.core.prompts import ANALYST_PROMPT

# LLM Modeli (Singleton olarak çağırıyoruz)
llm = get_llm(temperature=0.3)

def analyst_node(state: dict):
    """
    Finansal Analist Ajanı:
    Sorumluluğu: Kullanıcı sorusunu analiz etmek ve yanıt taslağı oluşturmak.
    """
    print("--- ANALİST ÇALIŞIYOR ---")
    
    messages = state["messages"]
    feedback = state.get("feedback", "")
    sender = state.get("sender", "")
    loop_count = state.get("loop_count", 0)

    # 1. Prompt Hazırlığı
    # Eğer Compliance ajanı bir önceki turda reddettiyse, uyarıyı ekle.
    if feedback and sender == "Compliance_Agent":
        print(f"⚠️ DÜZELTME TALEBİ ALINDI: {feedback}")
        system_content = f"{ANALYST_PROMPT}\n\n⚠️ DİKKAT: Bir önceki cevabın Risk Ekibi tarafından şu gerekçeyle reddedildi: '{feedback}'. Lütfen bu eleştiriyi dikkate alarak cevabını yeniden yaz."
    else:
        system_content = ANALYST_PROMPT

    # 2. Mesaj Listesini Oluştur
    # En başa Sistem Promptunu koyuyoruz, sonra konuşma geçmişi geliyor.
    final_messages = [SystemMessage(content=system_content)] + messages

    # 3. LLM Çağrısı
    response = llm.invoke(final_messages)

    # 4. State Güncelleme
    return {
        "messages": [response], # LangGraph bu yeni mesajı geçmişe ekleyecek
        "sender": "Analyst_Agent",
        "loop_count": loop_count + 1
    }