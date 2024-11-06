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
from ..schemas import ProcessedImagesResponse

router = APIRouter()
UPLOAD_DIR = r"backend\processed"

device = 'cuda' if torch.cuda.is_available() else 'cpu'
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large").to(device)
model_yolo = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True).to(device)

@router.post("/{image_id}")
async def process_image(image_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = db.execute(select(ImageDB).where(ImageDB.id == image_id))
    image_database = query.scalar_one_or_none()
    
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    if not image_database:
        raise HTTPException(status_code=404, detail="Image not found")

    try:
        img = cv2.imread(image_database.file_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = model_yolo(img_rgb)
        boxes = results.xyxy[0]
        boxes = boxes.cpu().numpy() if device == 'cuda' else boxes.numpy()
        os.makedirs(os.path.join(UPLOAD_DIR, str(current_user.id)), exist_ok=True)

        for i, box in enumerate(boxes):
            x1, y1, x2, y2, conf, cls = box.astype(int)
            segment = img[y1:y2, x1:x2]  

            segment_filename = f"{os.path.splitext(os.path.basename(image_database.file_path))[0]}_segment_{i}.png"
            segment_path = os.path.join(UPLOAD_DIR, str(current_user.id), segment_filename)
            cv2.imwrite(segment_path, segment)

            # Generate captions for the segment
            raw_image = Image.open(segment_path).convert('RGB')
            inputs = processor(raw_image, return_tensors="pt",
                                           max_length=80,           
                                            num_beams=7,    
                                            temperature=0.9,        
                                            top_k=80,                
                                            top_p=0.95,             
                                            repetition_penalty=2.0,   
                                            num_return_sequences=3).to(device)
            out = model.generate(**inputs)

            caption = processor.decode(out[0], skip_special_tokens=True)


            processed_image_db = ProcessedImage(
                file_path=segment_path,
                original_image_id=image_database.id,
                description=caption  
            )
            db.add(processed_image_db)

        image_database.is_processed = True
        db.add(image_database)
        db.commit()

        return JSONResponse(content={"message": "Image processed successfully", "file_path": image_database.file_path})

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to process image: {str(e)}"
        )
    
@router.get("/{image_id}", response_model=list[ProcessedImagesResponse])
async def getProcessedImages(image_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = db.execute(select(ProcessedImage).where(
        ProcessedImage.original_image_id == image_id))
    image_database = query.scalars().all()

    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )
    processed_images = [{"id": image.id,
                         "file_path": image.file_path,
                         "original_image_id": image.original_image_id,
                         "description": image.description,
                         "created_at": image.created_at,
                         "filepath_backend": "http://localhost:8000/processed-images"+image.file_path.replace("\\", "/").replace("backend", "").replace("processed", "")} for image in image_database]
    return processed_images