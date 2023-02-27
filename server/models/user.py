import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from server.db.base_class import Base


class User(Base):
    id = Column(Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    avatar = Column(String, default="")
    email = Column(String, unique=True, nullable=True)
    is_verified = Column(Boolean, default=False)
    disabled = Column(Boolean, default=False)
    providers = Column(String)
    hashed_password = Column(String)
    role = Column(String, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class EmailOtp(Base):
    id = Column(Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    email = Column(String)
    otp = Column(String)
    attempts = Column(Integer)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User")
