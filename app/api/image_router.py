import os
from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.utils.file_storage_utils import save_upload_file
from app.services.remove_background_service import process_remove_background
from app.services.pas_photo_service import process_pas_photo

router = APIRouter()

ALLOWED_MIME_TYPES = ["image/jpeg", "image/png", "image/jpg", "image/webp"]


# ---------------------------------------------------------------------------
# Helper: validate uploaded image and return (input_filepath) or raise
# ---------------------------------------------------------------------------
async def _validate_and_save(file: UploadFile) -> str:
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Format file tidak didukung. Harap upload JPG, PNG, atau WEBP.",
        )

    # Validate file size
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    max_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024
    if file_size > max_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"Ukuran file melebihi batas {settings.MAX_FILE_SIZE_MB}MB.",
        )

    return await save_upload_file(file)


# ---------------------------------------------------------------------------
# POST /api/image/remove-background
# ---------------------------------------------------------------------------
@router.post("/api/image/remove-background")
async def remove_background(file: UploadFile = File(...)):
    input_filepath = None
    try:
        input_filepath = await _validate_and_save(file)
        output_filename = await process_remove_background(input_filepath, file.filename)
        return {
            "success": True,
            "message": "Background berhasil dihapus",
            "data": {
                "file_name": output_filename,
                "download_url": f"/files/output/{output_filename}",
            },
        }
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Terjadi kesalahan saat memproses gambar."},
        )


# ---------------------------------------------------------------------------
# POST /api/image/pas-photo
# ---------------------------------------------------------------------------
@router.post("/api/image/pas-photo")
async def pas_photo(
    file: UploadFile = File(...),
    size: str = Form(...),
    background: str = Form(...),
):
    """
    Generate a passport-style (pas foto) image.

    Parameters
    ----------
    file       : uploaded photo (JPG / PNG / WEBP)
    size       : one of "2x3", "3x4", "4x6"
    background : one of "red", "blue"
    """
    from app.services.pas_photo_service import PAS_PHOTO_SIZES, BACKGROUND_COLORS

    # Validate enum values
    if size not in PAS_PHOTO_SIZES:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": f"Ukuran tidak valid. Pilihan: {', '.join(PAS_PHOTO_SIZES.keys())}",
            },
        )
    if background not in BACKGROUND_COLORS:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": f"Warna background tidak valid. Pilihan: {', '.join(BACKGROUND_COLORS.keys())}",
            },
        )

    input_filepath = None
    try:
        input_filepath = await _validate_and_save(file)
        output_filename = await process_pas_photo(
            input_filepath=input_filepath,
            original_filename=file.filename,
            size_key=size,
            bg_color_key=background,
        )
        return {
            "success": True,
            "message": "Pas foto berhasil dibuat",
            "data": {
                "file_name": output_filename,
                "download_url": f"/files/output/{output_filename}",
            },
        }
    except HTTPException:
        raise
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Terjadi kesalahan saat membuat pas foto."},
        )
