# routes/user.py
import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session

# from ..db import get_db
from ..models import User, Image
from ..schemas import ImageResponse

# from ..auth import get_current_user  # Assuming this function checks JWT and returns current user
from ..dependencies import get_db, get_current_user
from sqlalchemy.future import select


router = APIRouter()

UPLOAD_DIR = r"backend\upload"


@router.post("/", response_model=ImageResponse)
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

    # Create image entry in database
    db_image = Image(file_path=file_path,
                     owner_id=current_user.id,
                     is_processed=False)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)

    return {
        "id": db_image.id,
        "file_path":  db_image.file_path.replace("\\","/"),
        "file_name": db_image.file_path.split("/")[-1],
        "is_processed": db_image.is_processed,
        "created_at":db_image.created_at,
        "updated_at":db_image.updated_at
    }


@router.get("/", response_model=list[ImageResponse])
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


@router.get("/all", response_model=list[ImageResponse])
async def read_images(db: Session = Depends(get_db)):
    result = db.execute(select(Image))
    return result.scalars().all()


@router.get("/{image_id}", response_model=ImageResponse)
async def read_image(
    image_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    db_image = db.execute(select(Image).filter(
        Image.id == image_id)).scalars().first()
    if db_image is None or db_image.owner_id != current_user.id:
        raise HTTPException(
            status_code=404, detail="Image not found or you do not have permission"
        )
    return db_image


@router.put("/{image_id}", response_model=ImageResponse)
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

    db_image = db.execute(select(Image).filter(
        Image.id == image_id)).scalars().first()
    if db_image:
        db_image.file_path = file_path
        db.commit()
        db.refresh(db_image)
        return db_image
    if db_image is None or db_image.owner_id != current_user.id:
        raise HTTPException(
            status_code=404, detail="Image not found or you do not have permission"
        )

    return db_image


@router.delete("/{image_id}", response_model=ImageResponse)
async def delete_image_route(
    image_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )
    db_image = db.execute(select(Image).filter(
        Image.id == image_id)).scalars().first()
    if db_image:
        db.delete(db_image)
        db.commit()
        os.remove(db_image.file_path)
        return db_image
    if db_image is None or db_image.owner_id != current_user.id:
        raise HTTPException(
            status_code=404, detail="Image not found or you do not have permission"
        )
    return db_image
