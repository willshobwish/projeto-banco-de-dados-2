# app/schemas.py
from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    full_name: str | None = None
    role: str | None = None

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    hashed_password: str

class UserResponse(UserBase):
    id: int  # Include the ID in the response model

    class Config:
        orm_mode = True  # Enables compatibility with SQLAlchemy models

class Token(BaseModel):
    access_token: str
    token_type: str
