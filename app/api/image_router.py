import os
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.utils.file_storage_utils import save_upload_file
from app.services.remove_background_service import process_remove_background

router = APIRouter()

ALLOWED_MIME_TYPES = ["image/jpeg", "image/png", "image/jpg", "image/webp"]

"""
@router.post("/api/image/remove-background")
async def remove_background(file: UploadFile = File(...)):
    # 1. Validation
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
        
    if file.content_type not in ALLOWED_MIME_TYPES:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": "Format file tidak didukung. Harap upload JPG, PNG, atau WEBP."
            }
        )
        
    # Validation file size
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)
    
    max_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024
    if file_size > max_bytes:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": f"Ukuran file melebihi batas {settings.MAX_FILE_SIZE_MB}MB."
            }
        )

    input_filepath = None
    try:
        # 2. Save input file
        input_filepath = await save_upload_file(file)
        
        # 3. Process removal
        output_filename = await process_remove_background(input_filepath, file.filename)
        
        # 4. Return success response
        return {
            "success": True,
            "message": "Background berhasil dihapus",
            "data": {
                "file_name": output_filename,
                "download_url": f"/files/output/{output_filename}"
            }
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Terjadi kesalahan saat memproses gambar."
            }
        )
    finally:
        # Cleanup input file if you want, but usually it's better done via a cron/background job
        pass
"""
