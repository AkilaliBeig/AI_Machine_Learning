from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os



# Correct service imports
from .services.llm_service import LLMService
from .services.vector_db_service import VectorDBService
from .services.document_service import DocumentService
from .services.rag_service import RAGService


# Initialize FastAPI
app = FastAPI()

# Enable CORS (for Swagger UI & frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Storage folder
STORAGE_DIR = "storage"
os.makedirs(STORAGE_DIR, exist_ok=True)

# Initialize services
document_service = DocumentService(storage_dir=STORAGE_DIR)
vector_service = VectorDBService()
llm_service = LLMService(api_key="YOUR_GROQ_API_KEY")
rag_service = RAGService(vector_service, llm_service)

# Pydantic model
class QueryRequest(BaseModel):
    query: str

# Health endpoint
@app.get("/health")
def health():
    return {"status": "ok"}

# Upload endpoint
@app.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):
    content = await file.read()
    text = document_service.save_document(file.filename, content)
    vector_service.add_document(text)
    return {"message": "Uploaded + embedded", "filename": file.filename}

# Query endpoint
@app.post("/query")
def query_endpoint(data: QueryRequest):
    return rag_service.query(data.query)
