# Risk ve Uyum Ajanı (Node Mantığı).
print("COMPLIANCE MODULE LOADED")

from langchain_core.messages import HumanMessage
from app.core.config import get_llm
from app.core.prompts import COMPLIANCE_PROMPT

# Bu ajan denetçi olduğu için temperature 0 olmalı (Kesin ve Yaratıcısız)
llm = get_llm(temperature=0.0)

def compliance_node(state: dict):
    """
    Risk ve Uyum Ajanı:
    Sorumluluğu: Analistin cevabını etik, yasal ve güvenlik açısından denetlemek.
    """
    print("--- RİSK KONTROLÜ YAPILIYOR ---")
    
    # Analistin son ürettiği cevabı al
    last_message = state["messages"][-1]
    last_content = last_message.content

    # Denetim için özel bir prompt hazırla
    check_prompt = f"""
    {COMPLIANCE_PROMPT}

    Aşağıdaki metni yukarıdaki kurallara göre denetle:
    ---
    {last_content}
    ---
    """

    # LLM'e sor
    response = llm.invoke([HumanMessage(content=check_prompt)])
    result = response.content.strip()

    # Sonucu Analiz Et (APPROVED veya REJECTED)
    if "APPROVED" in result:
        print("✅ ONAYLANDI")
        return {
            "compliance_status": "APPROVED",
            "feedback": "",
            "sender": "Compliance_Agent"
        }
    else:
        # "REJECTED | Sebebini al"
        parts = result.split("|", 1)
        reason = parts[1].strip() if len(parts) > 1 else "Genel güvenlik ihlali."
        print(f"🛑 REDDEDİLDİ: {reason}")
        
        return {
            "compliance_status": "REJECTED", 
            "feedback": reason,
            "sender": "Compliance_Agent"
        }