from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserEdit(BaseModel):
    password: str


class User(UserBase):
    updated_at: Optional[datetime]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
