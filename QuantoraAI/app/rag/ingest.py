# PDF/Markdown dosyalarını okuyup vektöre çeviren script.
import os
import glob
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from app.rag.embeddings import get_embedding_model

# --- AYARLAR ---
DATA_PATH = "data/raw_pdfs"
DB_PATH = "data/vector_db"

def load_documents():
    """
    data/raw_pdfs klasöründeki PDF ve TXT dosyalarını okur.
    """
    documents = []
    
    # PDF'leri Bul
    pdf_files = glob.glob(f"{DATA_PATH}/*.pdf")
    for file in pdf_files:
        print(f"📄 Okunuyor: {file}")
        loader = PyPDFLoader(file)
        documents.extend(loader.load())

    # TXT/Markdown'ları Bul
    txt_files = glob.glob(f"{DATA_PATH}/*.txt") + glob.glob(f"{DATA_PATH}/*.md")
    for file in txt_files:
        print(f"📝 Okunuyor: {file}")
        loader = TextLoader(file, encoding="utf-8")
        documents.extend(loader.load())

    return documents

def ingest_data():
    """
    Belgeleri vektör veritabanına işler (Ana Fonksiyon).
    """
    # 1. Belgeleri Yükle
    docs = load_documents()
    if not docs:
        print("⚠️ HATA: İşlenecek belge bulunamadı! 'data/raw_pdfs' klasörüne dosya atın.")
        return

    # 2. Parçalara Böl (Chunking)
    # Finansal metinler için chunk size'ı dengeli tutuyoruz.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200, # Bağlam kopmasın diye örtüşme payı
        separators=["\n\n", "\n", " ", ""]
    )
    splits = text_splitter.split_documents(docs)
    print(f"🧩 Belgeler {len(splits)} parçaya bölündü.")

    # 3. Embedding Modelini Al
    embedding_model = get_embedding_model()

    # 4. Vektör Veritabanını Oluştur ve Kaydet
    print("💾 Vektör Veritabanı oluşturuluyor (Bu işlem biraz sürebilir)...")
    Chroma.from_documents(
        documents=splits,
        embedding=embedding_model,
        persist_directory=DB_PATH
    )
    print(f"✅ BAŞARILI! Veriler '{DB_PATH}' konumuna kaydedildi.")

if __name__ == "__main__":
    # Klasör yoksa oluştur
    os.makedirs(DATA_PATH, exist_ok=True)
    ingest_data()