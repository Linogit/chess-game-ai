FROM python:3.11-bookworm

# Installa le dipendenze di sistema necessarie per pygame e altre librerie
RUN apt-get update && apt-get install -y \
    libsdl2-2.0-0 \
    libsdl2-image-2.0-0 \
    libsdl2-mixer-2.0-0 \
    libsdl2-ttf-2.0-0 \
    libportmidi0 \
    && rm -rf /var/lib/apt/lists/*

# Imposta la directory di lavoro
WORKDIR /app

# Copia il file dei requisiti e installa le dipendenze Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia il codice dell'applicazione
COPY . .

# Imposta le variabili d'ambiente se necessario
ENV PYTHONPATH=/app/src

# NOTA: Stockfish è installato come servizio separato in docker-compose.yml
# quindi NON lo installiamo qui nel container principale