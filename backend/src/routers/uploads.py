import shutil
import os
from fastapi import APIRouter, UploadFile, File, HTTPException
import ulid

router = APIRouter(prefix="/uploads", tags=["uploads"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Generate a unique filename to avoid collisions
        # Use generic extension if missing
        _, file_extension = os.path.splitext(file.filename)
        if not file_extension:
             file_extension = ".bin"

        new_filename = f"{ulid.new()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, new_filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        return {"filename": new_filename, "url": f"/uploads/{new_filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
