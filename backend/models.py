# app/models.py
from sqlalchemy import Column, Integer, String,ForeignKey,Boolean,DateTime, func
from sqlalchemy.orm import relationship
from .db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    full_name = Column(String(255))
    hashed_password = Column(String(255))
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    images = relationship("Image", back_populates="owner")

class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String(300), nullable=False)
    is_processed = Column(Boolean,nullable=False,default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    owner = relationship("User", back_populates="images")
    processed_images = relationship("ProcessedImage", back_populates="original_image")
    
class ProcessedImage(Base):
    __tablename__ = "processed_images"
    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String(300), nullable=False)
    original_image_id = Column(Integer, ForeignKey("images.id"), nullable=False)
    description = Column(String(500),nullable=True)
    created_at = created_at = Column(DateTime, default=func.now(), nullable=False)
    
    # Relationship to the original image
    original_image = relationship("Image", back_populates="processed_images")