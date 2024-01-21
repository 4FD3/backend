---
page_type: OCR
description: "An OCR API that can be used to extract text information using the openCV and Tesseract"
languages:
- python
---


# Local Testing on Docker [1st way]

docker build --tag fastapi-ocr-intelli .

docker run --detach --publish 3100:3100 fastapi-ocr-intelli


# Local Testing without Docker [2nd way]

###  Install the requirements

apt-get install -y tesseract-ocr && apt-get install -y libgl1-mesa-glx

`pip install -r requirements.txt`

### Start the application

`uvicorn main:app --reload`

## Example call to access the application:

http://localhost:3100/

