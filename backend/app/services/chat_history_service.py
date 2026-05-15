from sqlalchemy.orm import Session

from app.models.chat_message import ChatMessage


class ChatHistoryService:
    def __init__(self, db: Session):
        self.db = db

    def save_message(
        self,
        user_id: int,
        document_id: int,
        role: str,
        content: str
    ):
        message = ChatMessage(
            user_id=user_id,
            document_id=document_id,
            role=role,
            content=content
        )

        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)

        return message

    def get_recent_messages(
        self,
        user_id: int,
        document_id: int,
        limit: int = 10
    ):
        messages = (
            self.db.query(ChatMessage)
            .filter(
                ChatMessage.user_id == user_id,
                ChatMessage.document_id == document_id
            )
            .order_by(ChatMessage.created_at.desc())
            .limit(limit)
            .all()
        )

        return list(reversed(messages))