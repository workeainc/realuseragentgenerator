FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY web/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY ua_generator.py .
COPY web/app.py .
COPY web/templates ./templates

# Create volume for SQLite database
VOLUME ["/app/data"]

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose port
EXPOSE 8000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
