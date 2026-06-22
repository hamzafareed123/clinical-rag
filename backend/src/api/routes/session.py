from fastapi import APIRouter
import uuid

router = APIRouter()
 

@router.post("/")
def create_session():
    session_id = uuid.uuid4().hex

    return {"session_id": session_id}
