# Use an official Python image as the basis
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside the container
EXPOSE 80

# Start landing_page.py when the container starts
CMD ["python", "landing_page.py"]