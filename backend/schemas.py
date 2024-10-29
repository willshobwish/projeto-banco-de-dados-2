# app/schemas.py
from pydantic import BaseModel
from datetime import datetime
class UserBase(BaseModel):
    email: str
    full_name: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

class Token(BaseModel):
    access_token: str
    token_type: str

class ImageResponse(BaseModel):
    id: int
    file_path: str
    is_processed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ProcessedImages(BaseModel):
    id:int
    file_path:str
    original_image_id:int
    description:str
    created_at:datetime

class ProcessedImagesResponse(ProcessedImages):
    filepath_backend:str