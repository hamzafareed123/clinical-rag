from fastapi import UploadFile, APIRouter, Form
from src.core.config import settings
from src.services.ingestor import ingest_document
import os
import aiofiles

router = APIRouter()


os.makedirs(settings.UPLOAD_DIR, exist_ok=True)


@router.post("/post-file")
async def post_file(file: UploadFile, session_id: str = Form(...)):

    file_path = os.path.join(settings.UPLOAD_DIR, file.filename)

    collection_name = f"session_{session_id}"

    content = await file.read()

    async with aiofiles.open(file_path, "wb") as f:
        await f.write(content)

    chunks = ingest_document(file_path, collection_name)

    return {
        "status": "success",
        "file Name": file.filename,
        "total-chunks": chunks,
    }
