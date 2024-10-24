from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    email: str
    name: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    image_filename: Optional[str] = None

    class Config:
        orm_mode = True
