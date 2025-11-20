# Utilizza l'immagine base ufficiale Python 3.11 versione slim
FROM python:3.11-slim

# Installa le dipendenze necessarie, inclusa Stockfish
RUN apt-get update && apt-get install -y \
    python3-pip \
    libsdl2-2.0-0 \
    libsdl2-image-2.0-0 \
    libsdl2-mixer-2.0-0 \
    libsdl2-ttf-2.0-0 \
    libportmidi0 \
    libswresample3 \
    libavformat58 \
    stockfish \
    && rm -rf /var/lib/apt/lists/*

# Imposta la working directory
WORKDIR /app

# Copia i file requirements e installa le dipendenze Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia il codice dell'applicazione
COPY . .

# Imposta le variabili d'ambiente per pygame in ambiente headless
ENV SDL_VIDEODRIVER=dummy
ENV SDL_AUDIODRIVER=disk
ENV XDG_RUNTIME_DIR=/tmp/runtime-root
RUN mkdir -p ${XDG_RUNTIME_DIR} && chmod 0700 ${XDG_RUNTIME_DIR}

# Comando di avvio
CMD ["python", "src/ChessGame.py"]
