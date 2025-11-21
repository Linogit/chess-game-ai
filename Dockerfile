FROM python:3.11-bookworm

RUN apt-get update && apt-get install -y \
    libsdl2-2.0-0 \
    libsdl2-image-2.0-0 \
    libsdl2-mixer-2.0-0 \
    libsdl2-ttf-2.0-0 \
    libportmidi0 \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Installa Stockfish - APPROCCIO SICURO
RUN cd /tmp && \
    wget -q https://files.stockfishchess.org/files/stockfish-16.1-linux.zip && \
    unzip -q stockfish-16.1-linux.zip && \
    mv stockfish-16.1-linux/Linux/stockfish-x64-avx2 /usr/local/bin/stockfish && \
    chmod +x /usr/local/bin/stockfish && \
    rm -rf stockfish-16.1-linux*

# Verifica che Stockfish sia installato
RUN ls -la /usr/local/bin/stockfish && /usr/local/bin/stockfish --version

COPY . .

ENV SDL_VIDEODRIVER=dummy
ENV SDL_AUDIODRIVER=disk
ENV XDG_RUNTIME_DIR=/tmp/runtime-root
RUN mkdir -p ${XDG_RUNTIME_DIR} && chmod 0700 ${XDG_RUNTIME_DIR}

CMD ["python", "src/ChessGame.py"]