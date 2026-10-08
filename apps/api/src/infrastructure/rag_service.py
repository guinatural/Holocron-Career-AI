import os
import chromadb
from chromadb.config import Settings
from langchain_aws import BedrockEmbeddings
import structlog
import uuid
import time

# O11y: Configuração de logs estruturados de classe Enterprise
logger = structlog.get_logger(__name__)

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
            
            # O11y: Observabilidade em embeddings na AWS
            logger.info("rag_service.init_bedrock", region=os.getenv("AWS_REGION", "us-east-1"), model="amazon.titan-embed-text-v1")
            
            self.embeddings = BedrockEmbeddings(
                model_id="amazon.titan-embed-text-v1",
                region_name=os.getenv("AWS_REGION", "us-east-1"),
                # Aqui entra a integração com LangSmith / AWS X-Ray Tracer na prop 'callbacks' em chamadas avançadas
            )
            
            self.resumes_collection = self.chroma_client.get_or_create_collection(
                name="user_resumes",
                metadata={"hnsw:space": "cosine"}
            )
            self.jobs_collection = self.chroma_client.get_or_create_collection(
                name="target_jobs",
                metadata={"hnsw:space": "cosine"}
            )
            logger.info("rag_service.started", status="success")
        except Exception as e:
            logger.error("rag_service.init_failed", error=str(e), exc_info=True)
            self.chroma_client = None

    def _trace_llm_execution(self, trace_id: str, operation: str, text_length: int):
        """Mock de injeção de traces O11y para chamadas de IA."""
        logger.info(
            "llm.execution.trace",
            trace_id=trace_id,
            operation=operation,
            payload_length=text_length,
            provider="aws_bedrock"
        )

    def inject_resume(self, user_id: str, resume_text: str, metadata: dict = None):
        if not self.chroma_client:
            raise ValueError("ChromaDB not initialized")
            
        trace_id = str(uuid.uuid4())
        start_time = time.time()
        
        self._trace_llm_execution(trace_id, "embed_resume", len(resume_text))
        
        vector = self.embeddings.embed_query(resume_text)
        
        meta = {"user_id": user_id, "type": "resume", "trace_id": trace_id}
        if metadata:
            meta.update(metadata)
            
        self.resumes_collection.add(
            embeddings=[vector],
            documents=[resume_text],
            metadatas=[meta],
            ids=[f"resume_{user_id}"]
        )
        
        duration = time.time() - start_time
        logger.info("rag_service.inject_resume", user_id=user_id, duration_sec=round(duration, 3))
        return True

    def match_resume_to_job(self, resume_text: str, top_k: int = 3):
        if not self.chroma_client:
            raise ValueError("ChromaDB not initialized")
            
        trace_id = str(uuid.uuid4())
        self._trace_llm_execution(trace_id, "match_job", len(resume_text))
        
        query_vector = self.embeddings.embed_query(resume_text)
        results = self.jobs_collection.query(
            query_embeddings=[query_vector],
            n_results=top_k
        )
        return results

rag_service = RAGService()
