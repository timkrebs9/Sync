# Dockerfile
FROM python:3.12-slim

# Arbeitsverzeichnis setzen
WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip

# Abhängigkeiten kopieren und installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Anwendungscode kopieren
COPY . .

# Create a script to handle environment variables
RUN echo '#!/bin/sh\n\
echo "DATABASE_URL=${DATABASE_URL}" > .env\n\
echo "POSTGRES_USER=${POSTGRES_USER}" >> .env\n\
echo "POSTGRES_PASSWORD=${POSTGRES_PASSWORD}" >> .env\n\
echo "POSTGRES_DB=${POSTGRES_DB}" >> .env\n\
echo "POSTGRES_PORT=${POSTGRES_PORT}" >> .env\n\
echo "STRIPE_SECRET_KEY=${STRIPE_SECRET_KEY}" >> .env\n\
echo "STRIPE_WEBHOOK_SECRET=${STRIPE_WEBHOOK_SECRET}" >> .env\n\
echo "STRIPE_PRICE_ID=${STRIPE_PRICE_ID}" >> .env\n\
echo "SECRET_KEY=${SECRET_KEY}" >> .env\n\
echo "ENCRYPTION_KEY=${ENCRYPTION_KEY}" >> .env\n\
echo "REDIS_URL=${REDIS_URL}" >> .env\n\
echo "FRONTEND_URL=${FRONTEND_URL}" >> .env\n\
uvicorn app.main:app --host 0.0.0.0 --port 8000' > /app/start.sh

RUN chmod +x /app/start.sh

# Port exponieren
EXPOSE 8000

CMD ["/app/start.sh"]