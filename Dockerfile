FROM python:3.13

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        ffmpeg \
        git \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements if exists, otherwise install Flask
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Set environment variables (optional)
ENV FLASK_APP=web.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the app
CMD ["python", "web.py"]
