# Use slim Python 3.11 as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (optional: only if needed by certain Python libs)
# RUN apt-get update && apt-get install -y gcc

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code after installing dependencies
COPY app/ app/
COPY .env .

# Expose the FastAPI default port
EXPOSE 8000

# Set environment variable for unbuffered logs (good for Docker)
ENV PYTHONUNBUFFERED=1

# Run the FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]