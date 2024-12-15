import email
from typing import Optional

from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    user_name: str
    nick_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    description: Optional[str] = None
    is_admin: int = 0
    is_active: int = 1


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    user_id: str
    create_time: datetime
    update_time: datetime

    class Config:
        orm_mode = True
        json_encoders = {datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")}


class UserInDB(UserInDBBase):
    id: int


class User(UserInDBBase):
    pass
