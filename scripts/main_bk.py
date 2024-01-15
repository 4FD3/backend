from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import cv2
import pytesseract
import os

app = FastAPI()

# Tesseract configuration (change the path accordingly)
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

# Ensure "uploads" folder exists or create it
uploads_folder = "uploads"
os.makedirs(uploads_folder, exist_ok=True)

@app.post("/process_receipt")
async def process_receipt(file: UploadFile = UploadFile(...)):
    try:
        # Save the received image
        image_path = f"uploads/{file.filename}"
        with open(image_path, "wb") as image:
            image.write(file.file.read())

        # Perform OCR using Tesseract and OpenCV
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)

        # Optional: Perform additional processing or parsing on the extracted text

        return JSONResponse(content={"text": text}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
