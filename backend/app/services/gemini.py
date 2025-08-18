import google.generativeai as genai
from dotenv import load_dotenv
from app.core.config import settings
import json

# Load .env
load_dotenv()

# Configure Gemini
genai.configure(api_key=settings.GOOGLE_API_KEY)
print("DEBUG GOOGLE_API_KEY:", settings.GOOGLE_API_KEY)

def query_gemini(prompt: str, context: list):
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    
    system_prompt = """You are a document assistant that provides answers in this exact JSON format:
    {
        "results": [{
            "document_id": "string",
            "theme": "string",
            "extracted_answer": "string",
            "citations": [{
                "filename": "string",
                "page": "number",
                "paragraph": "number",
                "sentence": "number"
            }]
        }]
    }"""

    try:
        # Format context more robustly
        formatted_context = []
        for idx, doc in enumerate(context):
            # Handle both ChromaDB v3 and v4 metadata formats
            metadata = doc.get("metadata", {}) if isinstance(doc, dict) else {}
            
            formatted_context.append({
                "document_id": doc.get("id", f"doc_{idx}"),
                "content": doc.get("document") or doc.get("content", ""),
                "metadata": {
                    "filename": metadata.get("filename", "unknown"),
                    "page": metadata.get("page", 0),
                    "paragraph": metadata.get("paragraph", 0),
                    "sentence": metadata.get("sentence", 0)
                }
            })

        # More explicit prompt engineering
        full_prompt = {
            "system_instruction": system_prompt,
            "context": formatted_context,
            "question": prompt,
            "requirements": [
                "Use ONLY the provided context",
                "Include ALL citation metadata exactly as provided",
                "Output MUST be valid JSON matching the given schema"
            ]
        }

        # Generate with timeout
        response = model.generate_content(
            json.dumps(full_prompt, indent=2),
            generation_config={
                "temperature": 0.3,
                "max_output_tokens": 2000
            },
            request_options={"timeout": 10}  # 10 second timeout
        )

        if not response.text:
            raise ValueError("Empty response from Gemini")

        # More robust JSON extraction
        raw_text = response.text.strip()
        json_str = raw_text.replace("```json", "").replace("```", "").strip()
        
        result = json.loads(json_str)
        
        # Validate response structure
        if not isinstance(result.get("results"), list):
            raise ValueError("Invalid response format: missing results array")
            
        return result

    except Exception as e:
        print(f"Gemini Error: {str(e)}")
        return {
            "results": [{
                "document_id": "error",
                "theme": "Error",
                "extracted_answer": f"Processing error: {str(e)}",
                "citations": []
            }]
        }