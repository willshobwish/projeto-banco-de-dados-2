from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import shutil
from pathlib import Path
from backend import crud, models, schemas, login, image_segmentation
from backend.database import engine, get_db
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "uploads/images"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists

@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), file: UploadFile | None = None):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    image_filename = None
    if file:
        image_filename = file.filename
        image_segmentation.save_image(file, UPLOAD_DIR)

    return crud.create_user(db=db, user=user, image_filename=image_filename)

@app.get("/users/", response_model=list[schemas.UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

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

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    crud.delete_user(db=db, user_id=user_id)
    return {"message": "User deleted successfully"}

@app.post("/login/")
async def login_user(form_data: schemas.UserCreate, db: Session = Depends(get_db)):
    user = login.authenticate_user(db, form_data.email, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Login successful"}
