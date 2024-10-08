# Use the official Python image as the base image
FROM python:alpine3.19

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Copy the FastAPI project code to the container
COPY . .

# Expose the port the app will run on
EXPOSE 8888

# Command to run the FastAPI app
CMD ["sh", "-c", "cd /app && python main.py"]
