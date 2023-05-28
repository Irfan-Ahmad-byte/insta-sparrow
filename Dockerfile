# Use an official Python runtime as a parent image
FROM python:3.10.11-alpine3.17

# Set the working directory in the container
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Copy the requirements.txt file to the working directory
COPY req.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r req.txt

# Copy the script and CSV file to the working directory
COPY script.py .
COPY followers_insta.csv .

# Make port 80 available to the world outside this container
EXPOSE 80

# Run your script when the container launches
CMD ["python", "get_insta_competitors.py"]

