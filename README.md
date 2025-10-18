# Face Verification API

A FastAPI-based service for verifying real human faces in images using DeepFace.

## Features

- Face detection using RetinaFace
- Validates exactly one real human face
- Returns confidence scores
- Handles various image formats
- Automatic file cleanup

## API Endpoints

- `GET /` - Health check and API info
- `GET /health` - Health status
- `GET /docs` - Interactive API documentation
- `POST /verify-face` - Upload image for face verification

## Deployment on Render.com

### Prerequisites

1. GitHub repository with this code
2. Render.com account

### Deployment Steps

1. **Connect to GitHub**
   - Go to [Render.com](https://render.com)
   - Sign up/Login with GitHub
   - Click "New +" → "Web Service"

2. **Configure Service**
   - **Name**: `face-verification-api`
   - **Environment**: `Python 3`
   - **Build Command**: `chmod +x build.sh && ./build.sh`
   - **Start Command**: `gunicorn main_prod:app -w 2 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`

3. **Environment Variables** (Optional)
   - `PYTHON_VERSION`: `3.9.16`

4. **Deploy**
   - Click "Create Web Service"
   - Wait for build to complete (5-10 minutes)
   - Your API will be available at the provided URL

### Testing the API

```bash
# Test health endpoint
curl https://your-app-name.onrender.com/health

# Test face verification
curl -X POST "https://your-app-name.onrender.com/verify-face" \
  -F "file=@/path/to/image.jpg"
```

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## API Response Format

**Success:**
```json
{
  "status": true,
  "message": "One real human face detected.",
  "face_confidence": 0.95
}
```

**Error:**
```json
{
  "status": false,
  "message": "Please upload an image with exactly one real face."
}
``` 