import os
import json
from google import genai
from PIL import Image
from dotenv import load_dotenv

# Load environment variable
load_dotenv()

# Inisialisasi Client menggunakan library terbaru (google-genai)
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def analyze_defect_with_gemini(text_query: str, image_path: str = None, context: str = ""):
    try:
        # Prompt system
        prompt = f"""You are an expert EPSON printer technician. Based on the following information, identify any defects or issues:

User Description: "{text_query}"
Knowledge Base Context: "{context}"

Provide your analysis in JSON format (no markdown, just plain JSON):
{{
  "defectDetected": boolean,
  "defectType": "string",
  "severity": "string ('low', 'medium', 'high', or 'critical')",
  "description": "string",
  "recommendedAction": "string",
  "confidence": number (0-1)
}}"""

        # Siapkan isi pesan
        contents = [prompt]

        # Jika ada gambar, sisipkan ke dalam array contents
        if image_path:
            try:
                img = Image.open(image_path)
                contents.insert(0, img)  # Letakkan gambar di urutan pertama
            except Exception as e:
                print(f"Error membuka gambar: {e}")

        # Panggil API Gemini dengan format terbaru
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=contents
        )
        
        response_text = response.text

        # Parsing JSON dari respons string
        clean_json_string = response_text.replace("```json", "").replace("```", "").strip()
        analysis_result = json.loads(clean_json_string)
        
        return analysis_result

    except Exception as e:
        print("Error pada Gemini Service:", e)
        return {
            "defectDetected": False,
            "defectType": "unknown",
            "severity": "low",
            "description": "Unable to analyze request",
            "recommendedAction": "Please try again or provide a clearer image.",
            "confidence": 0
        }