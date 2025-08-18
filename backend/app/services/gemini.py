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

    system_prompt = """
    You are a document assistant that provides answers in strict JSON format.
    Rules:
    - Always include the citation metadata (document_id, filename, page, paragraph, sentence).
    - "citations" must be taken directly from the context metadata, not invented.
    - Always output valid JSON only.
    Example format:
    {
        "results": [
            {
                "document_id": "uuid123",
                "theme": "Topic",
                "extracted_answer": "answer here",
                "citations": [
                    {
                        "filename": "doc1.pdf",
                        "page": 2,
                        "paragraph": 3,
                        "sentence": 1
                    }
                ]
            }
        ]
    }
    """

    # Pass both text and metadata to Gemini
    formatted_context = []
    for doc in context:
        formatted_context.append({
            "document_id": doc["id"],
            "filename": doc["metadata"].get("filename"),
            "page": doc["metadata"].get("page"),
            "paragraph": doc["metadata"].get("paragraph"),
            "sentence": doc["metadata"].get("sentence")      
        })

    full_prompt = f"""
    {system_prompt}

    Context Documents:
    {json.dumps(formatted_context, indent=2)}

    Question: {prompt}
    """

    try:
        response = model.generate_content(full_prompt)
        raw_text = response.text.strip()

        if raw_text.startswith("```json"):
            raw_text = raw_text[7:-3].strip()
        elif raw_text.startswith("```"):
            raw_text = raw_text[3:-3].strip()

        result = json.loads(raw_text)

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

