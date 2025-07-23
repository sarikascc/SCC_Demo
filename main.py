from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from deepface import DeepFace
import os
import shutil

app = FastAPI()

@app.post("/verify-face")
async def verify_face(file: UploadFile = File(...)):
    # Ensure temp folder exists
    os.makedirs("temp", exist_ok=True)
    file_path = os.path.join("temp", file.filename)

    # Save uploaded image
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
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

        return JSONResponse(status_code=400, content={
            "status": False,
            "message": "Face detection failed — likely cartoon, screen image, or no face.",
            "error": str(e)
        })
