# KI-GUI

## Export requirements pomocí poetry

`poetry export --without-hashes --format=requirements.txt > requirements.txt`

## Instalace projektu z github

1. `git clone <repo> -b here-we-start`
2. `cd <repo>`
3. `python -m venv .venv`
4. Pro Linux `source .venv/bin/activate`, Pro Windows `/.venv/Scripts/Activate.ps1` (popřípadě - activate.bat) - prosím ne windows `;)`
5. `pip install -r requirements.txt`

Z důvodu ušetření času. Ruff nebudeme instalovat do vscode.
Pojede se hezky z terminálu.

[Rules](https://docs.astral.sh/ruff/rules/)

1. `ruff check --watch` - Python Linter, hlídá  chyby v kódu podle rules viz. link
2. `ruff format` - Zformátuje kód podle knihovny Black

## Spuštění projektu v dockeru

projekt běží na adrese `0.0.0.0:8000`

`docker-compose up --build`

## Pokud nebude fungovat docker :)

`uvicorn api.main:app --reload` - spuštění projektu v uvicornu `--reload` při změně se znovu načtou změny
