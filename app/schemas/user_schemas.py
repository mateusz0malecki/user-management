from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Any

from auth.hash import Hash


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.password = Hash.get_password_hash(self.password)


class UserEdit(BaseModel):
    password: str

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.password = Hash.get_password_hash(self.password)


class User(UserBase):
    updated_at: Optional[datetime]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


class UserCheck(User):
    user_id: str
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True


class UserPagination(BaseModel):
    page_number: int = None
    page_size: int = None
    total_record_count: int = None
    pagination: dict = {}
    records: List[User] = []

    def __init__(self, users, first, last, page, page_size, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_number = page
        self.page_size = page_size
        self.total_record_count = len(users)
        self.records = users[first:last]

        if last >= len(users):
            self.pagination["next"] = None
        else:
            self.pagination["next"] = f"/users?page={page + 1}&page_size={page_size}"
        if page > 1:
            self.pagination["previous"] = f"/users?page={page - 1}&page_size={page_size}"
        else:
            self.pagination["previous"] = None
