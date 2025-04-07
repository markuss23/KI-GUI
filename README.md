# KI-GUI

## Export requirements pomocí poetry

`poetry export --without-hashes --format=requirements.txt > requirements.txt`

## Instalace projektu z github

1. `git clone <repo>`
2. `cd <repo>`
3. `python -m venv .venv`
4. Pro Linux `source .venv/bin/activate`, Pro Windows `/.venv/Scripts/Activate.ps1` (popřípadě - activate.bat)
5. `pip install -r requirements.txt`

## Spuštění projektu v dockeru

projekt běží na adrese `0.0.0.0:8000`

`docker-compose up --build`
