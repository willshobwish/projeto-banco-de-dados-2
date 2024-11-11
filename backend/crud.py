# app/crud.py
from .models import User
from .utils import hash_password
from hashlib import sha256


def hash_password(password: str):
    return sha256(password.encode('utf-8')).hexdigest()


def create_user(db, user):
    hashed_password = hash_password(user['password'])


    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO users (email, full_name, hashed_password, created_at, updated_at)
        VALUES (%s, %s, %s, NOW(), NOW())
    """, (user['email'], user['full_name'], hashed_password))

    db.commit()
    user_id = cursor.lastrowid  


    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    db_user = cursor.fetchone()

    cursor.close()
    return db_user

def get_user_by_email(db, email):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    db_user = cursor.fetchone()
    cursor.close()
    return db_user