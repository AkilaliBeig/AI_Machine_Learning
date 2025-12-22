# backend/main.py
import os
from dotenv import load_dotenv

# ✅ LOAD ENV BEFORE ANYTHING ELSE
load_dotenv()

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.services.document_service import DocumentService
from backend.services.vector_db_service import VectorDBService
from backend.services.llm_service import LLMService
from backend.services.rag_service import RAGService
from backend.services.chunking_service import TextSplitter


# ✅ VERIFY API KEY IMMEDIATELY
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("❌ GROQ_API_KEY not found. Check .env location.")

print("✅ GROQ_API_KEY loaded")

# -------------------------
# FastAPI App
# -------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Services (ORDER MATTERS)
# -------------------------
document_service = DocumentService(storage_dir="storage")
vector_service = VectorDBService()
llm_service = LLMService(api_key=GROQ_API_KEY)
rag_service = RAGService(vector_service, llm_service)

# -------------------------
# Models
# -------------------------
class QueryRequest(BaseModel):
    query: str

# -------------------------
# Routes
# -------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):
    content = await file.read()
    text = document_service.save_document(file.filename, content)
    splitter = TextSplitter(chunk_size=500, overlap=100)
    chunks = splitter.split_text(text, file.filename)
    vector_service.add_documents(chunks)


    return {
        "message": "Uploaded + embedded",
        "filename": file.filename,
        "chunks": len(chunks),
    }

@app.post("/query")
def query_docs(req: QueryRequest):
    return rag_service.query(req.query)
