from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.api.image_router import router as image_router
from app.core.config import settings
from app.utils.file_storage_utils import ensure_storage_dirs

# Ensure storage directories exist at startup
ensure_storage_dirs()

app = FastAPI(title="QuickTools Image Service")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files mapping
app.mount("/files/output", StaticFiles(directory=settings.STORAGE_OUTPUT_DIR), name="output_files")

# Health check
@app.get("/health")
def health_check():
    return {
        "success": True,
        "message": "Image service is running"
    }

# Include routers
app.include_router(image_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.SERVICE_PORT)
