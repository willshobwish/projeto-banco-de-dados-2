# app/main.py
from fastapi import FastAPI
from .database import Base, engine
from .routes import auth, protected, user, routes
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:8100",  # Allow your Ionic app
    # "http://localhost:3000",  # If you also use another frontend
    # Add any other origins you need to allow
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, prefix="/auth")
app.include_router(protected.router)
app.include_router(user.router, prefix="/users")
app.include_router(routes.router, prefix="/test")
