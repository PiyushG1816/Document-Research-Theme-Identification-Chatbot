import google.generativeai as genai
from dotenv import load_dotenv
from app.core.config import settings
import os
import json

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def query_gemini(prompt: str, context: list):
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    
    # Structured prompt for Gemini
    system_prompt = """
    You are a document assistant that provides answers in strict JSON format.
    Always return responses in this exact structure:
    {
        "results": [
            {
                "document_id": "unique_id",
                "theme": "main_topic",
                "extracted_answer": "concise_answer",
                "citations": ["source1", "source2"]
            }
        ]
    }
    """
    
    full_prompt = f"""
    {system_prompt}
    
    Context Documents:
    {json.dumps(context, indent=2)}
    
    Question: {prompt}
    """
    
    try:
        response = model.generate_content(full_prompt)
        raw_text = response.text.strip()
        
        # Clean JSON response
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:-3].strip()
        elif raw_text.startswith("```"):
            raw_text = raw_text[3:-3].strip()
            
        result = json.loads(raw_text)
        
        # Validate structure
        if "results" not in result:
            raise ValueError("Invalid response format")
            
        return result
        
    except Exception as e:
        return {
            "results": [{
                "document_id": "error",
                "theme": "Error",
                "extracted_answer": f"Could not process response: {str(e)}",
                "citations": []
            }]
        }
