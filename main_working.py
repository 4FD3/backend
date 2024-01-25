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
import re
import easyocr
import json

app = FastAPI()

# Ensure "uploads" folder exists or create it
uploads_folder = "uploads"
os.makedirs(uploads_folder, exist_ok=True)

# Serve static files (e.g., index.html) from the "static" directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/process_receipt")
async def process_receipt(file: UploadFile = UploadFile(...)):
    try:
        image_path = os.path.join(uploads_folder, file.filename)
        # Save the received image
        with open(image_path, "wb") as image:
            image.write(file.file.read())
        # Perform OCR using Tesseract and OpenCV
        image_to_ocr = cv2.imread(image_path)


        word_pattern = re.compile(r'\b\w+\b')  # Matches any word
        number_pattern = re.compile(r'\b\d+\.\d+\b(?! )')
        total_pattern = re.compile(r'TOTAL', re.IGNORECASE)  # Matches the word "TOTAL" (case-insensitive)

        #easyOCR
        reader = easyocr.Reader(['en'], gpu=False)
        results = reader.readtext(image_to_ocr)

        extracted_text = [result[1] for result in results]


        # Assuming 'extracted_text' is your list
        lowercase_text = [element.lower() for element in extracted_text]

        total_index = lowercase_text.index('total') if 'total' in lowercase_text else -1

        if total_index != -1:
            extracted_text = extracted_text[:total_index + 2]  # Keep elements before and after 'Total'
        else:
            extracted_text = extracted_text  # If 'Total' is not found, keep the original list

        # Extract the first line containing any word
        first_word_line = next((line.strip() for line in extracted_text if word_pattern.search(line)), None)

        extracted_text = [re.sub(r'(?<=\d),(?=\d)', '.', element.replace(' ', '').replace('s', '').replace('S', '').replace('O', '0').replace('o', '0')) for element in extracted_text]


        # Define regular expressions for patterns
        word_pattern = re.compile(r'\b\w+\b')  # Matches any word
        #number_pattern = re.compile(r'\d+\.\d+')  # Matches numbers in the form of x.y
        number_pattern = re.compile(r'\b\d+\.\d+\b')  # Matches numbers in the form of x.y

        total_pattern = re.compile(r'TOTAL', re.IGNORECASE)  # Matches the word "TOTAL" (case-insensitive)

        number_lines = [line.strip() for line in extracted_text if number_pattern.search(line)]

        total_line = next((line.strip() for line in extracted_text if total_pattern.search(line)), None)

        target_numbers = number_lines


        filtered_list = []

        for element in target_numbers:
            try:
                num = float(element)
                filtered_list.append(num)
            except ValueError:
                pass


        total = 0

        for i in range(len(filtered_list)):
            total = max(filtered_list)
            filtered_list.remove(total)
            
            sum_of_elements = sum(filtered_list)
            
            if total <= 0.2 * sum_of_elements + sum_of_elements:
                break

        # Create a dictionary for mapping
        items_list = {f"item_{i + 1}": num for i, num in enumerate(filtered_list)}

        # Create a dictionary for the result
        result_dict = {
            'store': first_word_line,
            "items":items_list,
            'total': total
        }

        # Convert the result dictionary to a JSON object
        result_json = json.dumps(result_dict, indent=2)
        return JSONResponse(content={"ocr_response": result_json}, status_code=200)
        
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

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)
