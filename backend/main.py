from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import shutil
from pathlib import Path
from backend import crud, models, schemas
from backend.database import engine, get_db
import os
from dotenv import load_dotenv

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads/images")

@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), file: UploadFile | None = None):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    image_filename = None
    if file:
        image_filename = file.filename
        with open(UPLOAD_DIR / image_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    return crud.create_user(db=db, user=user, image_filename=image_filename)

@app.get("/users/", response_model=list[schemas.UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    crud.delete_user(db=db, user_id=user_id)
    return {"message": "User deleted successfully"}
