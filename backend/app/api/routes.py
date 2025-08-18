from fastapi import APIRouter, UploadFile, File
from app.models.request import QueryRequest
from app.services.files import save_file
from app.services.chroma import store_document_in_chroma, collection, embedding_model
from app.services.gemini import query_gemini

router = APIRouter()

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_path = save_file(file)
    store_document_in_chroma(file_path, file.filename)
    return {"message": f"{file.filename} uploaded and processed with metadata"}

@router.post("/query/")
async def query_documents(request: QueryRequest):
    # Get relevant documents
    query_embedding = embedding_model.encode([request.query]).tolist()[0]
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=request.top_k,
        include=["ids", "documents", "metadatas"]
    )

    # Prepare context with explicit fields
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    ids = results["ids"][0]

    context = []
    for doc_id, d, m in zip(ids, docs, metas):
        context.append({
            "id": doc_id,
            "content": d,
            "filename": m.get("filename"),
            "page": m.get("page"),
            "paragraph": m.get("paragraph"),
            "sentence": m.get("sentence")
        })

    # Get structured response from Gemini
    return query_gemini(request.query, context)
