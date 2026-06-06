from sqlalchemy import Column, String, DateTime, ForeignKey, SmallInteger, Index, func, Date
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import uuid


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    todos = relationship("Todo", back_populates="user", cascade="all, delete-orphan")


class Todo(Base):
    __tablename__ = "todos"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(500), nullable=False)
    priority = Column(SmallInteger, default=1)  # 0=low, 1=medium, 2=high
    status = Column(String(20), default="pending")  # pending, in_progress, done
    due_date = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="todos")

    __table_args__ = (
        Index("idx_todos_user_status", "user_id", "status"),
    )
