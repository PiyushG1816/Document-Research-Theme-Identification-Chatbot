import google.generativeai as genai
from dotenv import load_dotenv
from app.core.config import settings
import os
import json

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def query_gemini(prompt: str):
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    response = model.generate_content(prompt)
    raw_text = response.text.strip()

    # Clean response
    if raw_text.startswith("```") and raw_text.endswith("```"):
        raw_text = "\n".join(raw_text.split("\n")[1:-1])
        if raw_text.strip().lower().startswith("json"):
            raw_text = "\n".join(raw_text.split("\n")[1:])

    try:
        return json.loads(raw_text)
    except:
        return {"error": "Invalid JSON", "raw": response.text}
