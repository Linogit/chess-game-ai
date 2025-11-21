FROM python:3.11-bookworm

RUN apt-get update && apt-get install -y \
    libsdl2-2.0-0 \
    libsdl2-image-2.0-0 \
    libsdl2-mixer-2.0-0 \
    libsdl2-ttf-2.0-0 \
    libportmidi0 \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Installa Stockfish usando un metodo diverso - scarica direttamente il binario
RUN wget -q -O /usr/local/bin/stockfish https://github.com/official-stockfish/Stockfish/releases/download/sf_16/stockfish-16-linux-x64 \
    && chmod +x /usr/local/bin/stockfish

# Verifica l'installazione
RUN ls -la /usr/local/bin/stockfish && echo "Stockfish installato correttamente"

COPY . .

ENV SDL_VIDEODRIVER=dummy
ENV SDL_AUDIODRIVER=disk
ENV XDG_RUNTIME_DIR=/tmp/runtime-root
RUN mkdir -p ${XDG_RUNTIME_DIR} && chmod 0700 ${XDG_RUNTIME_DIR}

CMD ["python", "src/ChessGame.py"]