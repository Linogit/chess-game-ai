from setuptools import setup, find_packages

setup(
    name="chess-ai",                     # Nome del pacchetto
    version="1.0.0",                     # Versione del progetto
    packages=find_packages(where="src"), # Trova automaticamente i pacchetti nella cartella src
    package_dir={"": "src"},             # Specifica che i pacchetti sono nella cartella src
    install_requires=[                   # Dipendenze necessarie per eseguire il progetto
        "pygame>=2.5.2",                 # Versione minima 2.5.2 di pygame
        "python-chess>=1.999",           # Versione minima 1.999 di python-chess
        "stockfish>=3.28.0",             # Versione minima 3.28.0 di stockfish
    ],
    python_requires=">=3.8",             # Richiede Python 3.8 o superiore
)
