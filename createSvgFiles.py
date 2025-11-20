import chess.svg          # Libreria per generare SVG degli scacchi
import os                 # Per operazioni sul filesystem

# Lista di tutti i pezzi degli scacchi (minuscolo = nero, maiuscolo = bianco)
pieces = ['p', 'P', 'r', 'R', 'n', 'N', 'k', 'K', 'q', 'Q', 'b', 'B']
# p/P = pedone, r/R = torre, n/N = cavallo, k/K = re, q/Q = regina, b/B = alfiere

dir = 'pieces_svg'        # Nome della cartella dove salvare i file SVG

# Crea la cartella se non esiste
if not os.path.exists(dir):
    os.mkdir(dir)

# Loop attraverso tutti i pezzi
for piece in pieces:
    # Genera l'immagine SVG del pezzo
    pie = chess.svg.piece(chess.Piece.from_symbol(piece))
    
    # Determina il colore del pezzo
    color = 'black'        # Pezzo nero (minuscolo)
    if piece.isupper():
        color = 'white'    # Pezzo bianco (maiuscolo)
    
    # Salva il file SVG
    with open(os.path.join(dir, f'{color}_{piece}.svg'), 'w') as f:
        f.write(pie)
