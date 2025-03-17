# KI-GUI

## Export requirements pomocí poetry

`poetry export --without-hashes --format=requirements.txt > requirements.txt`

## Instalace projektu z github

1. `git clone <repo>`
2. `cd <repo>`
3. `pip install virtualenv`
4. `virtualenv .venv`
5. `source .venv/bin/activate`
6. `pip install -r requirements.txt`

## Spuštění projektu v dockeru

projekt běží na adrese `0.0.0.0:8000`

`docker-compose up --build`

## 01

Obsah Prvího zachytnéo bodu.

- Co je to API
  - Rozdíly
- OpenAPI json + swagger
- FastApi vs Flask vs Django
- Poetry a proč?
- Ruff a proč?

## Co je to API?

Application Programming Interface (API) je soubor procedur, funkcí, protokolů a knihoven, který se využívá při vývoji softwaru.

Smyslem API je zajištění komunikace mezi dvěma platformami, které si vzájemně vyměňují data. Umožňují využívat již naprogramovaná řešení a integrovat je do vlastních webů či aplikací.

[Co je to api](https://www.rascasone.com/cs/blog/co-je-api)

## OpenAPI Specifikace (OAS) – Přehled

OpenAPI Specification (OAS) je standardizovaný jazyk pro popis HTTP API, který umožňuje konzistentní sdílení informací v celém životním cyklu API. Klíčové body zahrnují:

### Co je OpenAPI?

- Specifikační jazyk pro HTTP API, který je nezávislý na programovacím jazyce  
- Typicky se zapisuje ve formátu YAML nebo JSON  
- Umožňuje jasnou komunikaci schopností API mezi poskytovateli a spotřebiteli  
- Poskytuje standardizovaný slovník termínů odrážející běžné koncepty API  

### Role v životním cyklu API  

OAS slouží jako centrální zdroj během celého životního cyklu API:

- **Shromažďování požadavků**: Pomáhá vytvářet rané návrhy API v přenosném formátu  
- **Návrh**: Vytváří hmatatelné, verzovatelné artefakty před začátkem kódování  
- **Vývoj**: Podporuje generování kódu pro implementaci serverové části  
- **Konfigurace infrastruktury**: Automatizuje nastavení API brány a validační pravidla  
- **Zkušenost vývojářů**: Pohání dokumentaci, interaktivní prostředí a generování SDK  
- **Testování**: Umožňuje kontraktní testování a bezpečnostní ověření oproti specifikaci  

![alt text](./images/What-is-OpenAPI-Simple-API-Lifecycle-Vertical.png)

### Výhody  

- Poskytuje „jedinou verzi pravdy“ v celém životním cyklu API  
- Zrychluje vývoj díky automatizaci a generování kódu  
- Zlepšuje konzistenci mezi návrhem a implementací  
- Zvyšuje komfort vývojářů při práci s API  
- Podporuje jak přístup „API-first“, tak „code-first“  

OAS efektivně propojuje celý životní cyklus API tím, že poskytuje konzistentní způsob přenosu informací mezi jednotlivými fázemi. To organizacím pomáhá zajistit kvalitu a konzistenci při vývoji API.

[What is OpenAPI](https://www.openapis.org/what-is-openapi)

###

## FastAPI vs Django vs Flask

Při výběru frameworku pro vývoj webových aplikací nebo API v Pythonu se nejčastěji rozhodujeme mezi třemi hlavními nástroji – **FastAPI**, **Django** a **Flask**. Každý z nich má své specifické vlastnosti, které určují jejich vhodnost pro různé typy projektů.

### Přehledové srovnání

| **Parametr**               | **Django**                                                                                     | **FastAPI**                                                              | **Flask**                                                             |
|----------------------------|-----------------------------------------------------------------------------------------------|--------------------------------------------------------------------------|----------------------------------------------------------------------|
| **Typ**                    | Full-stack web framework                                                                      | Mikro-web framework                                                     | Mikro-web framework                                                  |
| **Využití**                | Vývoj komplexních webových aplikací a API                                                     | Vývoj API a mikroservis                                                 | Vývoj malých webových aplikací a jednoduchých API                   |
| **Výkon**                  | Rychlý při budování velkých aplikací                                                         | Velmi rychlý pro API a mikroservisy                                     | Pomalejší kvůli synchronnímu zpracování a ruční validaci            |
| **Škálovatelnost**         | Škálovatelný, ale ORM a šablonovací engine mohou zpomalit                                    | Vysoce škálovatelný díky asynchronnímu kódu a typovým anotacím          | Obtížně škálovatelný bez vestavěné podpory ORM a cachování          |
| **Náročnost na učení**     | Složitější pro začátečníky                                                                    | Jednoduché pro začátečníky                                              | Střední obtížnost                                                   |
| **Nástroje pro databáze**  | Komplexní sada (integrovaný ORM)                                                             | Omezená, žádná vestavěná podpora                                        | Omezená, žádná vestavěná podpora                                    |
| **Asynchronní programování** | Ano, přes `asyncio`, ale s nižší efektivitou                                               | Nativní podpora (rychlé díky Pydantic)                                  | Ne, nutné řešit externě                                             |
| **ORM (Object-relational mapping)** | Ano                                                                                | Ne                                                                      | Ne                                                                  |
| **Komunita**               | Velká a aktivní                                                                               | Malá, ale rychle rostoucí                                               | Velká a aktivní                                                     |
| **Dokumentace**            | Rozsáhlá a dobře udržovaná                                                                   | Menší, ale neustále se zlepšující                                       | Velká a snadno dostupná                                             |
| **Výhody**                 | Bezpečnost, škálovatelnost, flexibilita, rychlé prototypování, administrace                  | Výkon, rychlost vývoje API, asynchronní zpracování, OpenAPI/Swagger podpora | Flexibilita, jednoduchost, ideální pro malé aplikace a prototypy    |
| **Nevýhody**               | Komplexní pro začátečníky, náročnější na debugování, méně vhodné pro malé projekty            | Hlavní soubory mohou být nepřehledné, chybí vestavěná bezpečnost         | Chybí vestavěná podpora cachování, ORM a asynchronizace             |

[GeeksforGeeks – Comparison of FastAPI with Django and Flask](https://www.geeksforgeeks.org/comparison-of-fastapi-with-django-and-flask/)

---

## FastAPI

FastAPI je moderní, rychlý (vysoce výkonný) webový framework pro vývoj API v Pythonu. Využívá standardní Python type hinty a poskytuje snadný a intuitivní způsob, jak vytvářet robustní a výkonná rozhraní.

### Klíčové vlastnosti

- **Rychlost**  
  Velmi vysoký výkon, srovnatelný s NodeJS a Go (díky knihovnám Starlette a Pydantic). Patří mezi nejrychlejší Python frameworky.

- **Méně chyb**  
  Díky type hintům a automatické validaci snižuje množství chyb způsobených vývojáři přibližně o 40%. *

- **Intuitivní prostředí**  
  Skvělá podpora v moderních editorech – automatické doplňování kódu a méně času stráveného laděním.

- **Snadné použití a učení**  
  Navrženo pro jednoduché a rychlé osvojení. Minimalizuje potřebu čtení rozsáhlé dokumentace.

- **Stručný a přehledný kód**  
  Minimalizace duplicitního kódu, více funkcionalit z jednoho deklarovaného parametru a méně chyb při vývoji.

- **Robustní a připravený na produkci**  
  Automaticky generovaná interaktivní dokumentace (Swagger UI, ReDoc) podporuje efektivní vývoj i testování.

- **Standardizace**  
  Plná kompatibilita s otevřenými standardy pro API – OpenAPI (dříve Swagger) a JSON Schema.

![alt text](./images/process-ram.png)

[FastAPI – Oficiální dokumentace](https://fastapi.tiangolo.com/)

---

## HTTP

HTTP je protokol pro přenos dat mezi klientem a serverem. Funguje na principu požadavků a odpovědí.

## HTTP request methods

HTTP protokol definuje metody požadavků, označované jako HTTP slovesa, které určují účel a očekávaný výsledek požadavku. Metody mohou být bezpečné, idempotentní nebo kešovatelné.

### GET

- Metoda GET požaduje reprezentaci zadaného prostředku. Požadavky používající metodu GET by měly načítat pouze data a neměly by obsahovat obsah požadavku.

### POST

- Metoda POST odešle entitu zadanému prostředku, což často způsobí změnu stavu nebo vedlejší efekty na serveru.

### PUT

- Metoda PUT nahradí všechny aktuální reprezentace cílového prostředku obsahem požadavku.

### DELETE

- Metoda DELETE odstraní zadaný prostředek.

### PATCH

- Metoda PATCH aplikuje na prostředek částečné změny.
