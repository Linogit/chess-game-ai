FROM python:3.8-slim

# Installa le dipendenze di sistema necessarie per Pygame
RUN apt-get update && apt-get install -y \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    libjpeg-dev \
    libtiff5-dev \
    xvfb \
    stockfish \
    && rm -rf /var/lib/apt/lists/*

# Crea la directory dell'app
WORKDIR /app

# Copia i file requirements e installa le dipendenze Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia tutto il codice dell'applicazione
COPY . .

# Crea le directory necessarie
RUN mkdir -p pieces_svg pieces_png

# Genera i file SVG dei pezzi
RUN python createSvgFiles.py

# Imposta le variabili d'ambiente per Pygame in headless mode
ENV SDL_VIDEODRIVER=dummy
ENV SDL_AUDIODRIVER=disk
ENV XDG_RUNTIME_DIR=/tmp/runtime-root
ENV PYTHONPATH=/app/src

# Crea la directory per il runtime
RUN mkdir -p /tmp/runtime-root

# Comando per eseguire l'applicazione
CMD ["xvfb-run", "-a", "python", "src/ChessGame.py"]