# Chess Game Project
Un gioco di scacchi in Python con avversario AI che utilizza il motore Stockfish e l'interfaccia PyGame

## Features
- PyGame Interfaccia grafica 
- Stockfish integrazione con il motore scacchistico
- Gestione promozione pezzi
- Convalida e evidenziazione dello spostamento
- Rilevamento scacco/matto

## Requirements

- Python 3.8+
- Stockfish engine
- PyGame
- python-chess

## Installation

### Local Development
```bash
git clone <repository-url>
cd chess-game-project
pip install -r requirements.txt
python createSvgFiles.py
python src/ChessGame.py
Docker
bash
docker-compose up --build
Struttura Progetto
•	src/ - Source code
•	tests/ - Unit tests
•	pieces_png/ - PNG piece images
•	pieces_svg/ - Generated SVG pieces
CI/CD Pipeline
Questo progetto include CI/CD automatizzato con
•	Code linting (flake8, black)
•	Type checking (mypy)
•	Security scanning (bandit)
•	Unit testing (pytest)
•	Docker image building
