import os
import uuid
import shutil
from pathlib import Path
from fastapi import UploadFile

from app.core.config import settings

def ensure_storage_dirs():
    os.makedirs(settings.STORAGE_INPUT_DIR, exist_ok=True)
    os.makedirs(settings.STORAGE_OUTPUT_DIR, exist_ok=True)

def generate_unique_filename(original_filename: str, prefix: str = "", extension: str = None) -> str:
    unique_id = uuid.uuid4().hex[:8]
    if extension is None:
        extension = os.path.splitext(original_filename)[1]
    
    # Ensure extension starts with a dot
    if extension and not extension.startswith('.'):
        extension = f".{extension}"
        
    base_name = os.path.splitext(original_filename)[0][:20]  # truncate to avoid super long names
    
    # Clean filename
    clean_base = "".join(c for c in base_name if c.isalnum() or c in ('-', '_')).strip()
    
    return f"{prefix}{clean_base}-{unique_id}{extension}"

async def save_upload_file(upload_file: UploadFile) -> str:
    ensure_storage_dirs()
    filename = generate_unique_filename(upload_file.filename)
    filepath = os.path.join(settings.STORAGE_INPUT_DIR, filename)
    
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
        
    return filepath

def get_output_filepath(filename: str) -> str:
    ensure_storage_dirs()
    return os.path.join(settings.STORAGE_OUTPUT_DIR, filename)
