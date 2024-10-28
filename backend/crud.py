from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import User
from .schemas import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_user_by_email(db: AsyncSession, email: str):
    result = db.execute(select(User).filter(User.email == email))
    return result.scalars().first()

async def create_user(db: AsyncSession, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()  #  the commit
    db.refresh(db_user)  #  the refresh
    return db_user  # Return the created user

async def get_user(db: AsyncSession, user_id: int):
    result =  db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 10):
    result =  db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()  # Extract user objects

async def update_user(db: AsyncSession, user_id: int, user: UserCreate):
    db_user =  get_user(db, user_id)
    if db_user:
        db_user.email = user.email
        db_user.full_name = user.full_name
        db_user.hashed_password = pwd_context.hash(user.password)
        db_user.role = user.role
        db.commit()  #  the commit
        db.refresh(db_user)  #  the refresh
        return db_user
    return None

async def delete_user(db: AsyncSession, user_id: int):
    db_user =  get_user(db, user_id)
    if db_user:
        db.delete(db_user)  #  the delete
        db.commit()  #  the commit
        return db_user
    return None
