FROM python:3.12-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app ./app
# Vendored official form PDFs + field inventories (repo root /forms)
COPY forms /forms

# Persistent storage: attach a Railway volume (or bind mount) at /data.
ENV DATA_DIR=/data

EXPOSE 8000
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
