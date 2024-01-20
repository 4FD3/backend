#!/bin/bash

# Create and activate a virtual environment
python -m venv ocrproj
source ocrproj/bin/activate

#upgrade pip
#python -m pip install --upgrade pip

# Install Tesseract (for Ubuntu/Debian-based systems)
apt-get install tesseract-ocr

# Install required libraries
pip install fastapi uvicorn pytesseract opencv-python python-multipart


# Run the FastAPI server
uvicorn main:app  --host 0.0.0.0 --port 8000 --reload

# Deactivate the virtual environment
deactivate
