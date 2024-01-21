from fastapi import FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import os
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import cv2
import pytesseract
import json

app = FastAPI()

# Tesseract configuration (change the path accordingly)
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

# Ensure "uploads" folder exists or create it
uploads_folder = "uploads"
os.makedirs(uploads_folder, exist_ok=True)

# Serve static files (e.g., index.html) from the "static" directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/process_receipt")
async def process_receipt(file: UploadFile = UploadFile(...)):
    try:
        # Save the received image
        image_path = os.path.join(uploads_folder, file.filename)
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

# Endpoint to serve the index.html file
@app.get("/")
async def read_root():
    return FileResponse("templates/index.html", media_type="text/html")

# Redirection for Swagger UI
@app.get("/docs")
async def get_docs():
    return FileResponse("templates/index.html", media_type="text/html")

# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")

# @app.get("/", response_class=HTMLResponse)
# async def index(request: Request):
#     print('Request for index page received')
#     return templates.TemplateResponse('index.html', {"request": request})

# @app.get('/favicon.ico')
# async def favicon():
#     file_name = 'favicon.ico'
#     file_path = './static/' + file_name
#     return FileResponse(path=file_path, headers={'mimetype': 'image/vnd.microsoft.icon'})

# @app.post('/hello', response_class=HTMLResponse)
# async def hello(request: Request, name: str = Form(...)):
#     if name:
#         print('Request for hello page received with name=%s' % name)
#         return templates.TemplateResponse('hello.html', {"request": request, 'name':name})
#     else:
#         print('Request for hello page received with no name or blank name -- redirecting')
#         return RedirectResponse(request.url_for("index"), status_code=status.HTTP_302_FOUND)

if __name__ == '__main__':
    #uvicorn.run('main:app', host='0.0.0.0', port=3100)
    uvicorn.run('main:app', host='0.0.0.0', port=8000)	
	
