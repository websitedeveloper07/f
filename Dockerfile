# Base image with Python and PHP CLI
FROM python:3.11-slim

# Install PHP CLI
RUN apt-get update && apt-get install -y php-cli curl unzip git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir flask

# Expose Render port
EXPOSE 5000

# Start Flask server
CMD ["python", "app.py"]
