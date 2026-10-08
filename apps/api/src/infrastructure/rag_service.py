import os
import chromadb
from chromadb.config import Settings
from langchain_aws import BedrockEmbeddings
import logging

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        chroma_path = os.getenv("CHROMA_DB_PATH", "http://localhost:8000")
        try:
            if chroma_path.startswith("http"):
                host = chroma_path.split("//")[1].split(":")[0]
                port = int(chroma_path.split(":")[2])
                self.chroma_client = chromadb.HttpClient(
                    host=host, 
                    port=port,
                    settings=Settings(allow_reset=True)
                )
            else:
                self.chroma_client = chromadb.PersistentClient(path=chroma_path)
            
            # Utilize AWS Bedrock Embeddings for generating vector representations
            # Requires AWS_PROFILE or valid environment credentials
            self.embeddings = BedrockEmbeddings(
                model_id="amazon.titan-embed-text-v1",
                region_name=os.getenv("AWS_REGION", "us-east-1")
            )
            
            # Collections
            self.resumes_collection = self.chroma_client.get_or_create_collection(
                name="user_resumes",
                metadata={"hnsw:space": "cosine"}
            )
            self.jobs_collection = self.chroma_client.get_or_create_collection(
                name="target_jobs",
                metadata={"hnsw:space": "cosine"}
            )
            logger.info("ChromaDB Client and Collections Initialized.")
        except Exception as e:
            logger.error(f"Failed to initialize RAG Service: {e}")
            self.chroma_client = None

    def inject_resume(self, user_id: str, resume_text: str, metadata: dict = None):
        """Vectorize and store user resume in ChromaDB."""
        if not self.chroma_client:
            raise ValueError("ChromaDB not initialized")
            
        vector = self.embeddings.embed_query(resume_text)
        
        meta = {"user_id": user_id, "type": "resume"}
        if metadata:
            meta.update(metadata)
            
        self.resumes_collection.add(
            embeddings=[vector],
            documents=[resume_text],
            metadatas=[meta],
            ids=[f"resume_{user_id}"]
        )
        return True

    def inject_job_description(self, job_id: str, job_text: str, metadata: dict = None):
        """Vectorize and store target job in ChromaDB."""
        if not self.chroma_client:
            raise ValueError("ChromaDB not initialized")
            
        vector = self.embeddings.embed_query(job_text)
        
        meta = {"job_id": job_id, "type": "job"}
        if metadata:
            meta.update(metadata)
            
        self.jobs_collection.add(
            embeddings=[vector],
            documents=[job_text],
            metadatas=[meta],
            ids=[f"job_{job_id}"]
        )
        return True

    def match_resume_to_job(self, resume_text: str, top_k: int = 3):
        """Query jobs collection with a resume to find matches."""
        if not self.chroma_client:
            raise ValueError("ChromaDB not initialized")
            
        query_vector = self.embeddings.embed_query(resume_text)
        results = self.jobs_collection.query(
            query_embeddings=[query_vector],
            n_results=top_k
        )
        return results

    def match_job_to_resumes(self, job_text: str, top_k: int = 5):
        """Query resumes collection with a job description to find candidates."""
        if not self.chroma_client:
            raise ValueError("ChromaDB not initialized")
            
        query_vector = self.embeddings.embed_query(job_text)
        results = self.resumes_collection.query(
            query_embeddings=[query_vector],
            n_results=top_k
        )
        return results

rag_service = RAGService()
