
from src.core.config import settings
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
def retrieve_docs(query: str, k: int = 4) -> list:
    db = Chroma(
        embedding_function=embedding,
        persist_directory=settings.CHROMA_PATH
    )

    return db.similarity_search(query, k=k)
