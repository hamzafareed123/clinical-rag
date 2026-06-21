from fastapi import APIRouter
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from src.core.config import settings
from src.services.retriever import retrieve_docs

router = APIRouter()


llm = ChatGroq(
    model="llama-3.3-70b-versatile", api_key=settings.GROQ_API_KEY, temperature=0.2
)


class Question(BaseModel):
    query: str


class MedicalAnswer(BaseModel):
    answer: str = Field(description="The answer to the question")
    score: float = Field(description="Confidence score between 0 and 1")
    citations: list = Field(description="List of source for the answer")


structured_llm = llm.with_structured_output(MedicalAnswer)


@router.post("")
def user_query(request: Question):

    docs = retrieve_docs(request.query)
    context = "\n\n".join(
        [
            f"[{doc.metadata['source']} - Page {doc.metadata.get('page_label', 'N/A')}] {doc.page_content}"
            for doc in docs
        ]
    )

    prompt = f"""
        You are a medical assistant. Answer ONLY using the context below.
        If unsure, lower your confidence score.

          Context:
          {context}

          Question: {request.query}?
            """

    result = structured_llm.invoke(prompt)
    return result
