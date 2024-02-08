---
page_type: OCR
description: "This application utilizes Docker for containerization, Python 3.10, and FastAPI for backend development. Gunicorn enhances performance, while OpenCV and Tesseract handle image processing and OCR tasks. Uvicorn serves as the ASGI server, and HTML/CSS with Jinja2 Templates form the user interface. The tech stack enables efficient receipt text extraction from images, making it a scalable and modern application."
Tools/languages/libraries:
- python, Docker, FastAPI, OpenCV, Tesseract, Uvicorn, Jinja2, HTML/CSS
---


# Local Testing on Docker [1st way]

`docker build --tag fastapi-ocr-intelli .`

`docker run --detach --publish 3100:3100 fastapi-ocr-intelli`


# Local Testing without Docker [2nd way]

###  Install the requirements

apt-get install -y tesseract-ocr && apt-get install -y libgl1-mesa-glx

`pip install -r requirements.txt`

### Start the application

`uvicorn main:app --reload`
OR
`gunicorn main:app -c gunicorn.conf.py`
## Example call to access the application on:

### browser:

http://localhost:3100/

### curl:

curl -X POST -H "Content-Type: multipart/form-data" -F "file=@/path/to/image.png[/jpeg/jpg]" http://localhost:3100/process_receipt

### postman:

![Alt text](image.png)
