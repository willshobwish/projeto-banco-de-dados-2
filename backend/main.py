# app/main.py
from fastapi import FastAPI
from .db import Base, engine
from .routers import users,upload,process
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:8100",  # Allow your Ionic app
    "http://localhost:3000",  # If you also use another frontend
    # Add any other origins you need to allow
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

os.makedirs(r'backend\processed',exist_ok=True)
os.makedirs(r'backend\upload',exist_ok=True)

app.mount("/files", StaticFiles(directory="backend/upload"), name="files")
app.mount("/processed-images", StaticFiles(directory="backend/processed"), name="processed")

# Include routers
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(upload.router,prefix='/upload')
app.include_router(process.router,prefix="/process")