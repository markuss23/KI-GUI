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

![alt text](What-is-OpenAPI-Simple-API-Lifecycle-Vertical.png)

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

---

### FastAPI

- **Zaměření**: Vysokovýkonné moderní RESTful API a mikroservisy  
- **Architektura**: Mikro-web framework založený na **Pydantic** a **type hints**  
- **Klíčové vlastnosti**:
  - Asynchronní programování (`async`/`await`) nativně podporováno
  - Automaticky generovaná dokumentace API (OpenAPI + Swagger UI)
  - Validace a serializace dat pomocí Pydantic
  - Podpora standardů OpenAPI a JSON Schema  
- **Použití**:  
  - API-first přístup  
  - Vysoce výkonné a škálovatelné aplikace, mikroservisy  
- **Výhody**:  
  - Výborný výkon, nativní asynchronní podpora, snadné testování a validace  
- **Nevýhody**:  
  - Menší komunita, méně vestavěných komponent oproti Django  

---

### Django

- **Zaměření**: Plně vybavený framework pro komplexní webové aplikace  
- **Architektura**: Následuje architektonický vzor **Model-Template-View (MTV)** a princip **DRY (Don't Repeat Yourself)**  
- **Klíčové vlastnosti**:
  - Vestavěný ORM, autentizace, administrace, šablonovací engine  
  - Architektura Model-View-Template (MVT)  
  - Možnost rozšíření pomocí Django REST Framework (DRF) pro tvorbu API  
- **Použití**:  
  - Monolitické aplikace, systémy s komplexní logikou  
  - Rychlý vývoj webových aplikací s robustní backend logikou  
- **Výhody**:  
  - Široká funkcionalita, bezpečnost, velká komunita, rozsáhlá dokumentace  
- **Nevýhody**:  
  - Náročnější pro začátečníky, robustní architektura méně vhodná pro malé projekty  

---

### Flask

- **Zaměření**: Minimalistický framework pro webové aplikace a API  
- **Architektura**: Založený na **Werkzeug WSGI** toolkitu a **Jinja2** template enginu  
- **Klíčové vlastnosti**:
  - Flexibilní architektura s možností integrace rozšíření podle potřeby
  - Architektura Model-View-Controller (MVC)
  - Jednoduché routování, nízká režie  
  - Není určeno pro asynchronní operace (nutno doplnit knihovnami)  
- **Použití**:  
  - Prototypy, malé až středně velké aplikace  
  - Projekty, kde je požadována maximální kontrola nad architekturou  
- **Výhody**:  
  - Jednoduchost, rychlé nastavení, vysoká flexibilita  
- **Nevýhody**:  
  - Chybí vestavěná podpora ORM, cachování, asynchronního zpracování  

---

[GeeksforGeeks – Comparison of FastAPI with Django and Flask](https://www.geeksforgeeks.org/comparison-of-fastapi-with-django-and-flask/)
