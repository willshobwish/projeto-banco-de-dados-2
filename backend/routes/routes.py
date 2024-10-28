# app/routes/user.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def test():
    return {"message": "This is a test endpoint."}
