# Use the official Python base image with the desired Python version
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python application code into the container
COPY app.py .

# Expose the port on which your application runs (assuming it's 5000)
EXPOSE 5000

# Set the command to run your Python application
CMD ["python", "app.py"]

