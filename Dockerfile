
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Flask app
EXPOSE 3000

# Start the Flask app
CMD ["python", "main.py"]
