from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from deepface import DeepFace
import os
import shutil
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Face Verification API",
    description="API for verifying real human faces in images",
    version="1.0.0"
)

# Add CORS middleware for web applications
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Face Verification API is running",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "face-verification-api"}

@app.post("/verify-face")
async def verify_face(file: UploadFile = File(...)):
    # Validate file type
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=400, 
            detail="Please upload an image file (JPEG, PNG, etc.)"
        )
    
    # Validate file size (10MB limit)
    if file.size and file.size > 10 * 1024 * 1024:  # 10MB
        raise HTTPException(
            status_code=400, 
            detail="File size too large. Please upload an image smaller than 10MB."
        )
    
    # Ensure temp folder exists
    os.makedirs("temp", exist_ok=True)
    file_path = os.path.join("temp", file.filename)

    try:
        # Save uploaded image
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract faces using retinaface detector
        faces = DeepFace.extract_faces(
            img_path=file_path,
            detector_backend="retinaface",
            enforce_detection=True
        )

        # Remove the temp file
        os.remove(file_path)

        # Check for exactly one face
        if len(faces) != 1:
            return JSONResponse(status_code=400, content={
                "status": False,
                "message": "Please upload an image with exactly one real face."
            })

        face_confidence = faces[0].get("confidence", None)

        return {
            "status": True,
            "message": "One real human face detected.",
            "face_confidence": face_confidence
        }

    except Exception as e:
        # Clean up file on error
        if os.path.exists(file_path):
            os.remove(file_path)
        
        logger.error(f"Face detection error: {str(e)}")
        return JSONResponse(status_code=400, content={
            "status": False,
            "message": "Face detection failed — likely cartoon, screen image, or no face.",
            "error": str(e)
        })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000))) 