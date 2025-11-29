# Embedding model (BGE-M3) ayarları.

import os
from langchain_huggingface import HuggingFaceEmbeddings

# Embedding Modeli Ayarları
# BAAI/bge-m3: Çok dilli ve güçlü bir modeldir.
MODEL_NAME = "BAAI/bge-m3"

def get_embedding_model():
    """
    Embedding modelini yükler ve döndürür.
    Modeli her seferinde indirmemek için cache kullanır.
    """
    print(f"📥 Embedding Modeli Yükleniyor: {MODEL_NAME}...")
    
    embeddings = HuggingFaceEmbeddings(
        model_name=MODEL_NAME,
        model_kwargs={'device': 'cpu'}, # GPU varsa 'cuda' yapabilirsin
        encode_kwargs={'normalize_embeddings': True} # Kosinüs benzerliği için önemli
    )
    
    return embeddings
