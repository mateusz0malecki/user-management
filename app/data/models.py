import uuid

from fastapi import HTTPException, status

from sqlalchemy import Column, String, DateTime, Text, Boolean
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

from data.database import Base


class User(Base):
    __tablename__ = "users"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(32), unique=True)
    password = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<id: {self.id}, name: {self.name}>"

    @staticmethod
    def get_all_users(db):
        return db.query(User).all()

    @staticmethod
    def get_user_by_id(db, user_id):
        try:
            uuid_user = uuid.UUID(user_id, version=4)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user id, try again."
            )
        if str(uuid_user) == user_id:
            return db.query(User).filter(User.user_id == user_id)

    @staticmethod
    def get_user_by_username(db, username):
        return db.query(User).filter(User.username == username)
