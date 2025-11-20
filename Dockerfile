FROM python:3.11-slim

# Installa le dipendenze di sistema in un unico layer
RUN apt-get update && apt-get install -y \
    python3-pip \
    libsdl2-2.0-0 \
    libsdl2-image-2.0-0 \
    libsdl2-mixer-2.0-0 \
    libsdl2-ttf-2.0-0 \
    libportmidi0 \
    libswresample3 \
    libavformat58 \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# Installa Stockfish manualmente (versione Linux)
RUN wget https://stockfishchess.org/files/stockfish-16.1-linux-x64.zip \
    && unzip stockfish-16.1-linux-x64.zip \
    && mv stockfish-16.1-linux-x64/Linux/stockfish-x64-avx2 /usr/local/bin/stockfish \
    && chmod +x /usr/local/bin/stockfish \
    && rm -rf stockfish-16.1-linux-x64*

# Installa le dipendenze Python
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Configura ambiente
ENV SDL_VIDEODRIVER=dummy
ENV SDL_AUDIODRIVER=disk
ENV XDG_RUNTIME_DIR=/tmp/runtime-root
RUN mkdir -p ${XDG_RUNTIME_DIR} && chmod 0700 ${XDG_RUNTIME_DIR}

CMD ["python", "src/ChessGame.py"]