from fastapi import UploadFile,File,APIRouter
from src.core.config import settings
import os
import aiofiles


router = APIRouter()


os.getenv(settings.UPLOAD_DIR,exit_ok=True)

@router.post("/post-file")
async def post_file(file:UploadFile):
    
    file_path = os.path.join(settings.UPLOAD_DIR,file.filename)
    
    content = await file.read()
    
    async with aiofiles.open(file_path,"wb") as f:
        await f.write(content)
        

    return {"status":"success","file Name":file}                