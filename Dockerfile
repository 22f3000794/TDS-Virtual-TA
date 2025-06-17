# Base image with Python 3.10
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install OS-level dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    wget \
    curl \
    libopenblas-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy app files
COPY . .

# Expose port (FastAPI default with uvicorn)
EXPOSE 8000

# Run the FastAPI server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
