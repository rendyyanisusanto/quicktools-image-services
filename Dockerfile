# Use Python 3.11 slim for smaller image
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (no special libs needed for rembg usually, 
# but we might need libgl1-mesa-glx for some image libs if shared)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY app/ ./app/

# Create storage and model cache directories
RUN mkdir -p storage/input storage/output /root/.u2net

# EXPOSE 8002
EXPOSE 8002

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]
