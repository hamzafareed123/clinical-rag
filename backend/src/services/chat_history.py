from src.db.database import SessionLocal
from src.db.model import ChatHistory


def save_message(session_id: str, role: str, content: str):

    db = SessionLocal()

    try:
        new_chat = ChatHistory(session_id=session_id, role=role, content=content)

        db.add(new_chat)
        db.commit()
        db.refresh(new_chat)

    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()


def get_history(session_id: str):
    db = SessionLocal()

    try:
        return (
            db.query(ChatHistory)
            .filter(ChatHistory.session_id == session_id)
            .order_by(ChatHistory.created_at.desc())
            .limit(10)
            .all()
        )

    finally:
        db.close()
