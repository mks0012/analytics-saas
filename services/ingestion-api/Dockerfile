FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Fix: Use the correct relative path from the build context (root)
COPY services/ingestion-api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all service logic
COPY services/ /app/services/

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "services.ingestion-api.main:app", "--host", "0.0.0.0", "--port", "8000"]