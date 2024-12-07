# Dockerfile
FROM python:3.11-slim

# Arbeitsverzeichnis setzen
WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip

# Abhängigkeiten kopieren und installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Anwendungscode kopieren
COPY . .

# Port exponieren
EXPOSE 8000

# Umgebungsvariablen für Produktion
ENV PORT=8000
ENV HOST=0.0.0.0

# Starten der Anwendung mit Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]