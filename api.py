from fastapi import FastAPI, UploadFile, File, Form
from src.services.rag_pipeline import chatbot
import shutil
import os

app = FastAPI()

# Sama seperti di README: GET /api/health
@app.get("/api/health")
def health_check():
    return {"status": "AI Service is running ✅", "service": "Python Gemini Vision + FAISS"}

# Sama seperti di README: POST /api/analyze/combined
@app.post("/api/analyze/combined")
async def analyze_combined(
    description: str = Form(None), 
    image: UploadFile = File(None)
):
    image_path = None
    
    # Simpan file gambar sementara
    if image:
        image_path = f"temp_{image.filename}"
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
            
    # Panggil pipeline chatbot kamu
    analysis_result = chatbot(query_text=description, image_path=image_path)
    
    # Hapus gambar sementara
    if image_path and os.path.exists(image_path):
        os.remove(image_path)
        
    return {
        "success": True,
        "analysis": analysis_result,
        "message": "Defect analyzed successfully"
    }

# Jalankan server (mirip dengan node src/index.js)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)