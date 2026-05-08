from src.services.retrieval import retrieve
from src.services.gemini_service import analyze_defect_with_gemini
import json

def chatbot(query_text=None, image_path=None):
    query_text = query_text or ""
    
    # 1. RETRIEVAL (RAG): Ambil referensi dari dataset FAQ menggunakan FAISS
    # Jika query_text kosong (hanya kirim gambar), kita skip FAISS
    context = ""
    if query_text.strip():
        context = retrieve(query_text, top_k=1)
    
    # 2. GENERATION (Gemini): Kirim Gambar, Teks, dan Konteks FAISS ke Gemini
    # Gemini akan mensintesis masalahnya dan mengeluarkan JSON
    analysis = analyze_defect_with_gemini(
        text_query=query_text, 
        image_path=image_path, 
        context=context
    )

    return analysis