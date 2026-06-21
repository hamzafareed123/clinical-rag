from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from src.core.config import settings

embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def ingest_document(file):

    loader = PyPDFLoader(file)

    document = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=300, separators=["\n\n", "\n", " ", ""]
    )

    chunks = text_splitter.split_documents(document)

    db = Chroma.from_documents(
        documents=chunks, embedding=embedding, persist_directory=settings.CHROMA_PATH
    )

    return len(chunks)
