import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class EmailOtpBase(BaseModel):
    id: Optional[uuid.UUID]
    otp: Optional[str]
    email: Optional[EmailStr]
    user_id: Optional[str]
    attempts: Optional[str]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class EmailOtpCreate(EmailOtpBase):
    pass


class EmailOtpUpdate(EmailOtpBase):
    pass
