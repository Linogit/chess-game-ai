FROM python:3.11-bookworm

RUN apt-get update && apt-get install -y \
    libsdl2-2.0-0 \
    libsdl2-image-2.0-0 \
    libsdl2-mixer-2.0-0 \
    libsdl2-ttf-2.0-0 \
    libportmidi0 \
    stockfish \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV SDL_VIDEODRIVER=dummy
ENV SDL_AUDIODRIVER=disk
ENV XDG_RUNTIME_DIR=/tmp/runtime-root
RUN mkdir -p ${XDG_RUNTIME_DIR} && chmod 0700 ${XDG_RUNTIME_DIR}

CMD ["python", "src/ChessGame.py"]