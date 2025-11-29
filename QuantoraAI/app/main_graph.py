# LangGraph Orkestrasyon (Ana Beyin) kodu buraya gelecek.

import operator
from typing import Annotated, TypedDict, List
from langchain_core.messages import BaseMessage, HumanMessage

from langgraph.graph import StateGraph, END

# Hazırladığımız düğümleri (ajanları) import ediyoruz
from app.agents.analyst import analyst_node
from app.agents.compliance import compliance_node

# --- 1. STATE (HAFIZA) TANIMI ---
# Ajanlar arasında elden ele dolaşacak veri paketi
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add] # Tüm konuşma geçmişi
    sender: str              # Son mesajı kim attı?
    compliance_status: str   # "APPROVED", "REJECTED" veya "UNKNOWN"
    feedback: str            # Reddedilme sebebi
    loop_count: int          # Sonsuz döngü engellemek için sayaç

# --- 2. ROUTER (KARAR MEKANİZMASI) ---
def router(state: AgentState):
    """
    Compliance sonucuna göre rotayı belirleyen fonksiyon.
    """
    status = state.get("compliance_status")
    loop_count = state.get("loop_count", 0)

    # Güvenlik Kilidi: Eğer 3 kereden fazla red yerse sistemi durdur.
    if loop_count > 3:
        print("⚠️ DÖNGÜ LİMİTİ AŞILDI: İşlem sonlandırılıyor.")
        return END
    
    if status == "APPROVED":
        return END  # Onaylandıysa kullanıcıya dön
    else:
        return "Analyst" # Reddedildiyse Analiste geri dön

# --- 3. GRAPH KURULUMU ---
workflow = StateGraph(AgentState)

# Düğümleri Ekle
workflow.add_node("Analyst", analyst_node)
workflow.add_node("Compliance", compliance_node)

# Kenarları (Yolları) Bağla
workflow.set_entry_point("Analyst") # 1. Adım: Analist çalışır
workflow.add_edge("Analyst", "Compliance") # 2. Adım: Sonuç Compliance'a gider

# 3. Adım: Karar Anı (Conditional Edge)
workflow.add_conditional_edges(
    "Compliance",
    router,
    {
        END: END,           # Bitiş
        "Analyst": "Analyst" # Geri dönüş
    }
)

# Grafiği Derle
app = workflow.compile()

# --- 4. TEST ÇALIŞTIRMASI (MAIN) ---
if __name__ == "__main__":
    print("\n🚀 QuantoraAI Başlatılıyor (v1.0 - Alpha)...")
    print("Çıkış için 'q' veya 'exit' yazın.\n")

    while True:
        user_input = input("👤 Soru: ")
        if user_input.lower() in ["q", "exit"]:
            print("Görüşmek üzere!")
            break
        
        # Başlangıç Durumu
        initial_state = {
            "messages": [HumanMessage(content=user_input)],
            "sender": "User",
            "compliance_status": "UNKNOWN",
            "feedback": "",
            "loop_count": 0
        }

        print("\n⚙️  İşleniyor...\n")
        
        # Akışı Çalıştır (Stream)
        # Sadece en son çıkan cevabı (Final Output) yazdırmak için:
        try:
            for event in app.stream(initial_state):
                # Bu döngü her adımda (node çalıştığında) bilgi verir
                pass
            
            # Son mesajı al (app.stream state'i günceller ama biz en sonuncuyu manuel alalım veya event'ten yakalayalım)
            # LangGraph stream çıktısı event bazlıdır. 
            # En son 'messages' listesindeki son eleman Analist'in ONAYLANMIŞ cevabıdır.
            
            # Pratik olması için invoke kullanalım (son state'i döner)
            final_state = app.invoke(initial_state)
            print(f"🤖 QuantoraAI: {final_state['messages'][-1].content}\n")
            print("-" * 50)

        except Exception as e:
            print(f"❌ HATA: {e}")