FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

COPY backend /app/backend
COPY public /app/public
COPY vault /app/vault

ENV PYTHONPATH=/app/backend

EXPOSE 8000 8100 9000
