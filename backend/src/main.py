from fastapi import FastAPI
from src.api.routes import router

app = FastAPI(title="CLICICAL-RAG", version="1.0.0")

app.include_router(router)


@app.get("/helth")
def health():
    return {"Status": "ok"}
