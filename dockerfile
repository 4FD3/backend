FROM python:3.10

WORKDIR /code

COPY requirements.txt .

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr && apt-get install -y libgl1-mesa-glx



RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 3100

CMD ["gunicorn", "main:app"]
