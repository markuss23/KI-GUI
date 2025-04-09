# Solution for task 2

```python

class BookBase(BaseModel):
    title: str = Field(max_length=255, min_length=3)
    author: str = Field(max_length=255, min_length=3)
    year: int = Field(ge=0)
    genre: str = Field(max_length=255, min_length=3)


class Book(BookBase):
    book_id: int


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    title: str | None = Field(default=None, max_length=255, min_length=3)
    author: str | None = Field(default=None, max_length=255, min_length=3)
    year: int | None = Field(default=None, ge=0)
    genre: str | None = Field(default=None, max_length=255, min_length=3)


class Message(BaseModel):
    message: str


books: list[Book] = [
    Book(
        book_id=1,
        title="The Great Gatsby",
        author="F. Scott Fitzgerald",
        year=1925,
        genre="Novel",
    ),
    Book(book_id=2, title="1984", author="George Orwell", year=1949, genre="Dystopian"),
    Book(
        book_id=3,
        title="To Kill a Mockingbird",
        author="Harper Lee",
        year=1960,
        genre="Novel",
    ),
]


ID_BOOK_PATH_ANNOTATION = Annotated[
    int, Path(description="ID of the Book", gt=0, le=9223372036854775000)
]


@app.get("/books")
def get_all_books() -> list[Book]:
    return [Book.model_validate(book) for book in books]


@app.post("/books")
def create_book(book: BookCreate) -> Book:
    book_data = book.model_dump()
    book_data["book_id"] = (books[-1].book_id + 1) if books else 1
    new_book: Book = Book.model_validate(book_data)
    books.append(new_book)
    return new_book


@app.get("/books/{book_id}")
def get_book(book_id: ID_BOOK_PATH_ANNOTATION) -> Book:
    for book in books:
        if book.book_id == book_id:
            return Book.model_validate(book)
    raise HTTPException(status_code=404, detail="Book not found")


@app.put("/books/{book_id}")
def update_book(book_id: ID_BOOK_PATH_ANNOTATION, updated_book: BookUpdate) -> Book:
    for i, book in enumerate(books):
        if book.book_id == book_id:
            book_data = book.model_dump()
            updated_data = updated_book.model_dump(exclude_unset=True, exclude_none=True)
            book_data.update(updated_data)
            
            final_book: Book = Book.model_validate(book_data)
            books[i] = final_book
            return final_book
    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{book_id}")
def delete_book(book_id: ID_BOOK_PATH_ANNOTATION) -> Message:
    for book in books:
        if book.book_id == book_id:
            books.remove(book)
            return Message(message="Book deleted successfully")
    raise HTTPException(status_code=404, detail="Book not found")

```
