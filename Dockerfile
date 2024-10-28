# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any necessary dependencies
RUN pip install --no-cache-dir fastapi uvicorn chromadb

# Expose port 8001 for FastAPI
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
