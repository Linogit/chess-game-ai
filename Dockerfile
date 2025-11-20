# Utilizza l'immagine base ufficiale Python 3.11 versione slim
FROM python:3.11-slim

# Installa le dipendenze di sistema
RUN apt-get update && apt-get install -y \
    libsdl2-2.0-0 \
    libsdl2-image-2.0-0 \
    libsdl2-mixer-2.0-0 \
    libsdl2-ttf-2.0-0 \
    stockfish \
    && rm -rf /var/lib/apt/lists/*

# Imposta la directory di lavoro
WORKDIR /app

# Copia e installa le dipendenze Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia il codice sorgente
COPY src/ ./src/
COPY pieces_png/ ./pieces_png/

# Genera i file SVG
RUN mkdir -p pieces_svg
COPY createSvgFiles.py .
RUN python createSvgFiles.py

# Comando di avvio
CMD ["python", "src/ChessGame.py"]