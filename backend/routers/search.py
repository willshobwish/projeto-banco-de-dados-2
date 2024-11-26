from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from ..dependencies import get_db, get_current_user
from ..models import ProcessedImage, User,Image
from ..schemas import ImageResponse  # Assuming you have a schema for processed images

router = APIRouter()

@router.get("/")
async def search_processed_images(
    query: str = Query(..., description="The description or keyword to search for"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Search for processed images by their description.
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )
    
    # Search query in the database
    search_query = f"%{query}%"
    results = (
        db.execute(
            select(ProcessedImage)
            .join(Image, Image.id == ProcessedImage.original_image_id)
            .filter(Image.owner_id == current_user.id)  # Filter images by the owner_id of the user
            .filter(ProcessedImage.description.ilike(search_query))  # Filter by description
        )
        .scalars()
        .all()
    )

    if not results:
        raise HTTPException(status_code=404, detail="No matching images found.")

    # Convert results into a response format
    return [
        {"id": image.id,
        "file_path": image.file_path,
        "original_image_id": image.original_image_id,
        "description": image.description,
        "created_at": image.created_at,
        "filepath_backend": "http://localhost:8000/processed-images"+image.file_path.replace("\\", "/").replace("backend", "").replace("processed", "")} for image in results
    ]
