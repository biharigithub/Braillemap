# Use official Python image
FROM python:3.11-slim

# Install system dependencies and tesseract for Hindi and English
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-hin \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && apt-get clean

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install Python packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port
EXPOSE 5000

# Run the Flask app using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
