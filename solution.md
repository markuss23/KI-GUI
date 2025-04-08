# Řešení

``` python
# In-memory databáze knih
books = [
    {
        "id": 1,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "year": 1925,
        "genre": "Novel",
    },
    {
        "id": 2,
        "title": "1984",
        "author": "George Orwell",
        "year": 1949,
        "genre": "Dystopian",
    },
    {
        "id": 3,
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "year": 1960,
        "genre": "Novel",
    },
]


@app.get("/books")
def get_all_books() -> list[dict[]]:
    return books


@app.post("/books")
def create_book(book: dict[]) -> dict[]:
    book_id = len(books) + 1
    book["id"] = book_id
    books.append(book)
    return book


@app.get("/books/{book_id}")
def get_book(book_id: int) -> dict[]:
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.put("/books/{book_id}")
def update_book(book_id: int, updated_book: dict[]) -> dict[]:
    for book in books:
        if book["id"] == book_id:
            book.update(updated_book)
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{book_id}")
def delete_book(book_id: int) -> dict[]:
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")
```
