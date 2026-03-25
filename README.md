# Image Service — Python Microservice

FastAPI-based microservice for image processing tools in QuickTools, focusing on background removal.

## Architecture

This service handles heavy Python-based image processing (`rembg`) and is called exclusively by the Node.js backend gateway — **never directly by the frontend**.

```
Frontend → Backend (Node.js :4000) → Python Image Service (:8002)
```

## Tech Stack

- Python 3.11+
- FastAPI + Uvicorn
- rembg (Background Removal)
- Pillow (Image handling)
- pydantic-settings

## Setup

### 1. Create virtual environment

```bash
cd python-services/image-service
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
# Default port is 8002
```

### 4. Run the service

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload
```

Service will be available at: `http://localhost:8002`

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/api/image/remove-background` | Remove background from image |
| GET | `/files/output/{filename}` | Download processed image |
| GET | `/docs` | Interactive API docs (Swagger UI) |
