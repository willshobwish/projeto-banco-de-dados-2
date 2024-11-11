import os
import requests
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import cv2
import torch
from ..models import User, ProcessedImage
from ..models import Image as ImageDB
from ..dependencies import get_db, get_current_user
from fastapi.responses import JSONResponse
from sqlalchemy.future import select

router = APIRouter()
UPLOAD_DIR = r"backend\processed"

device = 'cuda' if torch.cuda.is_available() else 'cpu'
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large").to(device)
model_yolo = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True).to(device)

@router.post("/{image_id}")
async def process_image(image_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    cursor = db.cursor(dictionary=True)

    # Query to fetch the image from the database
    cursor.execute("""
        SELECT * FROM images WHERE id = %s
    """, (image_id,))
    image_database = cursor.fetchone()

    if not image_database:
        raise HTTPException(status_code=404, detail="Image not found")

    try:
        # Read and process the image with OpenCV
        img = cv2.imread(image_database["file_path"])
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = model_yolo(img_rgb)
        boxes = results.xyxy[0]
        boxes = boxes.cpu().numpy() if device == 'cuda' else boxes.numpy()

        os.makedirs(os.path.join("backend/upload", str(current_user["id"])), exist_ok=True)

        for i, box in enumerate(boxes):
            x1, y1, x2, y2, conf, cls = box.astype(int)
            segment = img[y1:y2, x1:x2]

            segment_filename = f"{os.path.splitext(os.path.basename(image_database['file_path']))[0]}_segment_{i}.png"
            segment_path = os.path.join("backend/upload", str(current_user["id"]), segment_filename)
            cv2.imwrite(segment_path, segment)

            # Generate captions for the segment
            raw_image = Image.open(segment_path).convert('RGB')
            inputs = processor(raw_image, return_tensors="pt", max_length=80, num_beams=7, temperature=0.9, top_k=80, top_p=0.95, repetition_penalty=2.0, num_return_sequences=3).to(device)
            out = model.generate(**inputs)
            caption = processor.decode(out[0], skip_special_tokens=True)

            # Insert processed image into the database
            cursor.execute("""
                INSERT INTO processed_images (file_path, original_image_id, description)
                VALUES (%s, %s, %s)
            """, (segment_path, image_database["id"], caption))
            db.commit()

        # Mark the original image as processed
        cursor.execute("""
            UPDATE images
            SET is_processed = TRUE
            WHERE id = %s
        """, (image_database["id"],))
        db.commit()

        cursor.close()
        db.close()

        return {"message": "Image processed successfully", "file_path": image_database["file_path"]}

    except Exception as e:
        cursor.close()
        db.close()
        raise HTTPException(
            status_code=500, detail=f"Failed to process image: {str(e)}"
        )
    
def get_processed_images(image_id: int, current_user: dict, db: Session = Depends(get_db)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )
    
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM processed_images 
        WHERE original_image_id = %s
    """, (image_id,))

    processed_images_db = cursor.fetchall()

    processed_images = [
        {
            "id": image["id"],
            "file_path": image["file_path"],
            "original_image_id": image["original_image_id"],
            "description": image["description"],
            "created_at": image["created_at"],
            "filepath_backend": "http://localhost:8000/processed-images" + image["file_path"].replace("\\", "/").replace("backend", "").replace("processed", "")
        }
        for image in processed_images_db
    ]

    cursor.close()
    db.close()

    return processed_images