# Cvičení: Pydantic a FastAPI - Validace dat a modely

## Cíl cvičení
Pochopení a použití Pydantic modelů, validátorů a FastAPI. Toto cvičení navazuje na základní koncepty z `api/main.py`.

## Zadání

Vytvořte REST API pro správu produktů v e-shopu s následujícími požadavky:

1. Rozšiřte základní aplikaci z `main.py` o Pydantic modely:
   - `Product` - model produktu s validátory
   - `Category` - model pro kategorii produktu
   - `ApiResponse` - model pro standardizované odpovědi API

2. Pro model `Product` implementujte:
   - Validaci ceny (musí být kladná)
   - Validaci názvu (minimální a maximální délka)
   - Validaci SKU kódu (pomocí regulárního výrazu)

3. Vytvořte CRUD endpointy:
   - `GET /products` - získání všech produktů s možností filtrování
   - `GET /products/{product_id}` - získání detailu produktu
   - `POST /products` - vytvoření nového produktu
   - `PUT /products/{product_id}` - aktualizace produktu
   - `DELETE /products/{product_id}` - odstranění produktu

4. Zajistěte správné použití `model_validate` metody při vracení dat z API

## Šablona pro řešení

```python
from typing import Annotated, List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field, field_validator
import re
from datetime import datetime

# Vytvoření instance FastAPI
app = FastAPI(title="Produktové API", docs_url="/")

# Simulovaná databáze - použijte pro uložení produktů
products_db = []
next_product_id = 1

# Anotace pro ID a parametry stránkování
ID_PATH_ANNOTATION = Annotated[int, Path(description="ID produktu", ge=1)]
LIMIT_QUERY_ANNOTATION = Annotated[int, Query(description="Počet položek na stránku", ge=1, le=100)]
OFFSET_QUERY_ANNOTATION = Annotated[int, Query(description="Posun stránkování", ge=0)]

# TODO: Implementujte Pydantic modely
class Category(BaseModel):
    # TODO: Implementujte model kategorie
    pass

class Product(BaseModel):
    # TODO: Implementujte model produktu s validátory
    # Nezapomeňte na validaci ceny, názvu a SKU kódu
    pass

class ApiResponse(BaseModel):
    # TODO: Implementujte model pro API odpovědi
    # (například success, message, data)
    pass

# CRUD endpointy
@app.get("/products")
def get_all_products(
    limit: LIMIT_QUERY_ANNOTATION = 10,
    offset: OFFSET_QUERY_ANNOTATION = 0,
    category: Optional[str] = None
) -> List[Product]:
    """
    Získání seznamu produktů s možností filtrování
    
    Použijte model_validate pro konverzi dat na Pydantic objekty při vracení
    """
    # TODO: Implementujte získání seznamu produktů a použijte model_validate
    pass

@app.post("/products")
def create_product(product: Product) -> Product:
    """
    Vytvoření nového produktu
    """
    # TODO: Implementujte vytvoření produktu
    # Nezapomeňte na přidělení ID a uložení do databáze
    pass

@app.get("/products/{product_id}")
def get_product(product_id: ID_PATH_ANNOTATION) -> Product:
    """
    Získání detailu produktu podle ID
    """
    # TODO: Implementujte získání produktu podle ID
    # Použijte model_validate pro konverzi dat z DB na Pydantic objekt
    pass

@app.put("/products/{product_id}")
def update_product(product_id: ID_PATH_ANNOTATION, product: Product) -> Product:
    """
    Aktualizace existujícího produktu
    """
    # TODO: Implementujte aktualizaci produktu
    pass

@app.delete("/products/{product_id}")
def delete_product(product_id: ID_PATH_ANNOTATION) -> ApiResponse:
    """
    Odstranění produktu
    """
    # TODO: Implementujte odstranění produktu
    # Vraťte ApiResponse s informací o úspěšném smazání
    pass
```

## Nápovědy

### Vytvoření validátorů pro Pydantic model

<details>
    <summary>Ukázka validátoru ceny</summary>

```python
@field_validator('price')
@classmethod
def validate_price(cls, v: float) -> float:
    if v <= 0:
        raise ValueError('Cena musí být kladné číslo')
    return v
```
</details>

<details>
    <summary>Ukázka validátoru SKU kódu</summary>

```python
@field_validator('sku')
@classmethod
def validate_sku(cls, v: str) -> str:
    pattern = r'^[A-Z]{3}-\d{4}-[A-Z]{2}$'
    if not re.match(pattern, v):
        raise ValueError('Neplatný formát SKU. Očekávaný formát: XXX-0000-XX')
    return v
```
</details>

### Použití model_validate při vrácení dat

<details>
    <summary>Ukázka použití model_validate</summary>

```python
# Převod dat z databáze na Pydantic model
product_data = {"id": 1, "name": "Telefon", "price": 599.99, "sku": "ABC-1234-XY", "category": "Electronics"}
product = Product.model_validate(product_data)
return product
```
</details>

### Implementace filtrace v endpointu GET /products

<details>
    <summary>Ukázka implementace filtrování</summary>

```python
@app.get("/products")
def get_all_products(
    limit: LIMIT_QUERY_ANNOTATION = 10,
    offset: OFFSET_QUERY_ANNOTATION = 0,
    category: Optional[str] = None
) -> List[Product]:
    filtered_products = products_db
    
    if category:
        filtered_products = [p for p in filtered_products if p["category"] == category]
    
    paginated = filtered_products[offset:offset + limit]
    
    # Použití model_validate_list pro konverzi seznamu slovníků na seznam Pydantic objektů
    return [Product.model_validate(product) for product in paginated]
```
</details>