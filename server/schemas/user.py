import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    id: Optional[uuid.UUID]
    avatar: Optional[str]
    email: Optional[EmailStr]
    is_verified: Optional[bool]
    role: Optional[str] = "member"
    providers: Optional[str]
    hashed_password: Optional[str]

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str


class RespUser(BaseModel):
    id: Optional[str] = None
    email: Optional[EmailStr] = None
    avatar: Optional[str] = None
    is_verified: Optional[bool] = None
    providers: Optional[str] = None
    role: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    token: Optional[Token]


class User(BaseModel):
    hashed_password: Optional[str] = None
    email: Optional[EmailStr] = None


class UserCreateInput(BaseModel):
    email: EmailStr
    password: str


class VerifyOTP(BaseModel):
    email: EmailStr
    otp: str


class UserInDB(User):
    hashed_password: str


class UserIn(User):
    password: str


class IdTokenLoginInput(BaseModel):
    id_token: str


class IdTokenValidteLoginInput(BaseModel):
    email: EmailStr


class IdTokenRegisterInput(BaseModel):
    id_token: str


class EmailSchema(BaseModel):
    email: EmailStr


class UserProfile(BaseModel):
    id: Optional[str] = None
    email: Optional[EmailStr] = None
    avatar: Optional[str] = None
    role: Optional[str] = None


class ChangePassword(BaseModel):
    old_password: str
    new_password: str


class ResetPassword(BaseModel):
    email: EmailStr
    otp: str
    new_password: str
