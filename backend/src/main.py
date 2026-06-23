from fastapi import FastAPI
from src.api.routes import router
from contextlib import asynccontextmanager
from src.db.database import create_table


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_table()
    yield


app = FastAPI(title="CLINICAL-RAG", version="1.0.0", lifespan=lifespan)

app.include_router(router)


@app.get("/health")
def health():
    return {"Status": "ok"}
