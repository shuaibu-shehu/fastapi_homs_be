# Use Python slim image
FROM python:3.11-slim

# Install system dependencies for building certain Python packages
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    build-essential \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the FastAPI project code to the container
COPY . .

# Expose the port the app will run on
EXPOSE 8888

# Command to run the FastAPI app
CMD ["sh", "-c", "cd /app && python3 main.py"]
