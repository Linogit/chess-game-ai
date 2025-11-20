 # Utilizza l'immagine base ufficiale Python 3.11 versione slim (leggera)
FROM python:3.11-slim

# Install system dependencies
# Aggiorna i repository dei pacchetti e installa le dipendenze di sistema necessarie
RUN apt-get update && apt-get install -y \
    libsdl2-2.0-0 \          # Libreria SDL2 per multimedia (necessaria per PyGame)
    libsdl2-image-2.0-0 \    # Estensione SDL2 per il supporto immagini
    libsdl2-mixer-2.0-0 \    # Estensione SDL2 per il supporto audio
    libsdl2-ttf-2.0-0 \      # Estensione SDL2 per il supporto font TrueType
    stockfish \              # Motore scacchistico AI (dipendenza di sistema)
    && rm -rf /var/lib/apt/lists/*  # Pulisce la cache per ridurre le dimensioni dell'immagine

# Imposta la directory di lavoro all'interno del container
WORKDIR /app

# Copia il file requirements.txt dalla macchina host al container
COPY requirements.txt .

# Installa tutte le dipendenze Python elencate in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt  # --no-cache-dir riduce le dimensioni

# Copia il codice sorgente dell'applicazione
COPY src/ ./src/                    # Copia tutta la cartella src/
COPY pieces_png/ ./pieces_png/      # Copia le immagini PNG dei pezzi degli scacchi

# Crea la directory per i file SVG e genera i pezzi degli scacchi in formato SVG
RUN mkdir -p pieces_svg             # Crea la cartella pieces_svg (se non esiste)
COPY createSvgFiles.py .            # Copia lo script per generare i file SVG
RUN python createSvgFiles.py        # Esegue lo script per generare i pezzi SVG

# Specifica il comando di avvio predefinito quando il container viene eseguito
CMD ["python", "src/ChessGame.py"]    # Avvia l'applicazione ChessGame