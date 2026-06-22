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
    session_id: str


class MedicalAnswer(BaseModel):
    answer: str = Field(description="The answer to the question")
    score: float = Field(description="Confidence score between 0 and 1")
    citations: list = Field(description="List of source for the answer")


structured_llm = llm.with_structured_output(MedicalAnswer)


@router.post("")
def user_query(request: Question):

    collection_name = f"session_{request.session_id}"
    print(collection_name)

    docs = retrieve_docs(request.query, collection_name)
    print(docs)

    context = "\n\n".join(
        [
            f"[{doc.metadata['source']} - Page {doc.metadata.get('page_label', 'N/A')}] {doc.page_content}"
            for doc in docs
        ]
    )

    print("context", context)

    prompt = f"""
        You are a medical assistant. Answer ONLY using the context below.
        If unsure, lower your confidence score.

          Context:
          {context}

          Question: {request.query}?
            """

    answer = structured_llm.invoke(prompt)

    return {
        "answer": answer.answer,
        "score": answer.score,
        "citations": answer.citations,
        "session Id": request.session_id,
    }
