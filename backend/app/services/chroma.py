import os, uuid, re
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# Directories
CHROMA_DIR = "chroma_db"
os.makedirs(CHROMA_DIR, exist_ok=True)

# Embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Chroma client
client = chromadb.Client(Settings(persist_directory=CHROMA_DIR))
collection = client.get_or_create_collection("documents")

def split_text_with_metadata(pages, chunk_size=500):
    chunks = []
    for page_num, page_text in pages:
        paragraphs = [p.strip() for p in page_text.split("\n") if p.strip()]
        for para_idx, para in enumerate(paragraphs, start=1):
            sentences = re.split(r'(?<=[.!?]) +', para)
            current_chunk, current_length = [], 0
            sentence_counter = 1
            for sentence in sentences:
                current_chunk.append(sentence)
                current_length += len(sentence) + 1
                if current_length >= chunk_size:
                    chunks.append({
                        "text": " ".join(current_chunk),
                        "page": page_num,
                        "paragraph": para_idx,
                        "sentence": sentence_counter - len(current_chunk) + 1
                    })
                    current_chunk, current_length = [], 0
                sentence_counter += 1
            if current_chunk:
                chunks.append({
                    "text": " ".join(current_chunk),
                    "page": page_num,
                    "paragraph": para_idx,
                    "sentence": sentence_counter - len(current_chunk)
                })
    return chunks

def store_document_in_chroma(file_path: str, filename: str):
    from services.ocr import extract_text_from_pdf, extract_text_from_image

    if filename.lower().endswith(".pdf"):
        pages = extract_text_from_pdf(file_path)
    elif filename.lower().endswith((".png", ".jpg", ".jpeg")):
        pages = extract_text_from_image(file_path)
    elif filename.lower().endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        pages = [(1, text)]
    else:
        return

    chunks = split_text_with_metadata(pages, chunk_size=500)
    embeddings = embedding_model.encode([c["text"] for c in chunks]).tolist()

    for i, chunk in enumerate(chunks):
        collection.add(
            ids=[str(uuid.uuid4())],
            documents=[chunk["text"]],
            embeddings=[embeddings[i]],
            metadatas=[{
                "filename": filename,
                "chunk_id": i,
                "page": chunk["page"],
                "paragraph": chunk["paragraph"],
                "sentence": chunk["sentence"]
            }]
        )
