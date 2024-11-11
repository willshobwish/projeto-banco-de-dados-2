# routes/user.py
import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session

from datetime import datetime

# from ..db import get_db
from ..models import User, Image

# from ..auth import get_current_user  # Assuming this function checks JWT and returns current user
from ..dependencies import get_db, get_current_user
from sqlalchemy.future import select


router = APIRouter()

UPLOAD_DIR = r"backend\upload"


@router.post("/")
async def upload_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )
    # Save the file to the upload directory
    file_path = os.path.join(UPLOAD_DIR, str(current_user.id), file.filename)
    os.makedirs(os.path.join(UPLOAD_DIR, str(current_user.id)), exist_ok=True)

    with open(file_path, "wb") as image_file:
        image_file.write(await file.read())

# Insert the image record into the database
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO images (file_path, owner_id, is_processed, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s)
    """, (file_path, current_user['id'], False, datetime.now(), datetime.now()))
    db.commit()
    image_id = cursor.lastrowid
    cursor.close()
    db.close()

    return {
        "id": image_id,
        "file_path": file_path.replace("\\", "/"),
        "file_name": file.filename,
        "is_processed": False,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }


@router.get("/")
async def read_images(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )
    result = (
        db.execute(select(Image).filter(Image.owner_id == current_user.id))
        .scalars()
        .all()
    )
    image_data = [
        {
            "id": image.id,
            "file_path":  'http://localhost:8000/files/'+image.file_path.replace("\\","/").replace("backend/","").replace("upload/",""),
            "is_processed": image.is_processed,
            "created_at":image.created_at,
            "updated_at":image.updated_at
        }
        for image in result
    ]
    return image_data
    # return await get_images(db, owner_id=current_user.id)


@router.get("/all")
async def read_images(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM images WHERE owner_id = %s", (current_user['id'],))
    images = cursor.fetchall()
    cursor.close()
    db.close()

    return [
        {
            "id": image["id"],
            "file_path": f"http://localhost:8000/files/{image['file_path'].replace('backend/', '').replace('upload/', '')}",
            "is_processed": image["is_processed"],
            "created_at": image["created_at"],
            "updated_at": image["updated_at"]
        } for image in images
    ]


@router.get("/{image_id}")
async def read_image(
    image_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM images WHERE id = %s AND owner_id = %s", (image_id, current_user['id']))
    image = cursor.fetchone()
    cursor.close()
    db.close()

    if not image:
        raise HTTPException(status_code=404, detail="Image not found or unauthorized")

    return image


@router.put("/{image_id}")
async def update_image_route(
    image_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    # Save the file to the upload directory
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as image_file:
        image_file.write(await file.read())

    cursor = db.cursor()
    cursor.execute("UPDATE images SET file_path = %s, updated_at = %s WHERE id = %s AND owner_id = %s",
                   (file_path, datetime.now(), image_id, current_user['id']))
    db.commit()
    cursor.close()
    db.close()

    return {"message": "Image updated successfully"}


@router.delete("/{image_id}")
async def delete_image_route(
    image_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM images WHERE id = %s AND owner_id = %s", (image_id, current_user['id']))
    image = cursor.fetchone()

    if not image:
        cursor.close()
        db.close()
        raise HTTPException(status_code=404, detail="Image not found or unauthorized")

    # Delete all processed images and the original file
    cursor.execute("DELETE FROM processed_images WHERE original_image_id = %s", (image_id,))
    os.remove(image["file_path"])

    cursor.execute("DELETE FROM images WHERE id = %s", (image_id,))
    db.commit()
    cursor.close()
    db.close()

    return {"message": "Image deleted successfully"}
