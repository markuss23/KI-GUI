<!-- markdownlint-disable MD033 -->

# 02 CRUD operace s knihami pomocí Pydantic

Vytvořte REST API pomocí FastAPI pro správu knih. Implementujte všechny CRUD operace (Create, Read, Update, Delete) s využitím Pydantic modelů pro validaci dat.

Vaše řešení by mělo zahrnovat:

- Definici vhodných Pydantic modelů pro knihy (základní model, model pro vytváření, model pro aktualizaci)  
- Vytvoření umělé databáze knih uložené v paměti  
- Implementaci následujících endpointů:
  - Získání seznamu všech knih
  - Přidání nové knihy
  - Získání konkrétní knihy podle ID
  - Aktualizace existující knihy
  - Smazání knihy

Pro validaci vstupů použijte vhodné validátory (např. minimální/maximální délka řetězce, minimální hodnota pro rok vydání).

<details>
<summary>Nápověda</summary>

```python
class BookBase(BaseModel):
    # Definujte základní vlastnosti knihy s validacemi
    pass

class Book(BookBase):
    # Přidejte ID knihy
    pass

class BookCreate(BookBase):
    # Model pro vytváření nové knihy
    pass

class BookUpdate(BookBase):
    # Model pro aktualizaci knihy, kde všechna pole jsou volitelná
    pass

# Umělá databáze knih
books: list[Book] = [
    # Přidejte několik knih pro testování
]

@app.get("/books")
def get_all_books() -> list[Book]:
    # Implementujte načtení všech knih
    pass

@app.post("/books")
def create_book(book: BookCreate) -> Book:
    # Implementujte vytvoření nové knihy
    pass

@app.get("/books/{book_id}")
def get_book(book_id: int) -> Book:
    # Implementujte získání konkrétní knihy podle ID
    pass

@app.put("/books/{book_id}")
def update_book(book_id: int, updated_book: BookUpdate) -> Book:
    # Implementujte aktualizaci knihy
    pass

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    # Implementujte smazání knihy
    pass
```
</details>
