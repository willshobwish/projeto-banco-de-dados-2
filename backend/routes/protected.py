# app/routes/protected.py
from fastapi import APIRouter, Depends
from ..dependencies import get_current_user

router = APIRouter()

@router.get("/protected")
async def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": "This is a protected route", "user": current_user}
