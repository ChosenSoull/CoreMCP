# Use an official Python runtime as a parent image
# Based on the project targeting Python 3.14
FROM python:3.14-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# We assume requirements.txt contains dependencies like 'ddgs' and 'playwright'
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application source code into the container at /app
COPY . .

# Expose the port the MCP server runs on (from main.py)
EXPOSE 44321

# Define the command to run the application when the container starts
# This runs main.py, which starts the MCP server
CMD ["python", "main.py"]