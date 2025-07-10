FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        gcc \
        python3-dev \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY backend/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ /app/

# Copy migration script and utilities
COPY migrate_images_to_s3.py /app/
COPY scripts/wait-for-it.sh /app/
COPY scripts/test-s3-connectivity.py /app/scripts/
RUN chmod +x /app/wait-for-it.sh

# Create directory for static files
RUN mkdir -p /app/staticfiles

# Expose port
EXPOSE 8000

# Copy entrypoint script
COPY scripts/backend-entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
