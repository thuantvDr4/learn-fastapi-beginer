
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import IntEnum
from uuid import UUID

app = FastAPI()

class Book(BaseModel):
    id: int = Field(..., description='Unique identifier of the book')
    title: str = Field(..., min_length=1, max_length=512, description='Title of the book')
    author: str = Field(..., min_length=1, max_length=512, description='Author of the book')
    description: str = Field(..., min_length=1, max_length=1000, description='Description of the book')
    rating: int = Field(gt=0, lt=6, description='The rating of the book')


class BookCreate(Book):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, description='Title of the book')
    author: Optional[str] = Field(..., description='Author of the book')
    description: Optional[str] = Field(..., min_length=1, max_length=1000, description='Description of the book')
    rating: Optional[int] = Field(...,gt=0, lt=6, description='The rating of the book')


all_books = [
]
@app.get("/")
def index():
    return {'message': 'Hello Book Project'}

@app.get("/books/")
def get_all_books(limit: int  = None):
    if not limit:
        return all_books
    else:
        return all_books[:limit]

@app.get("/books/{id}", response_model = Book)
def get_book(id:int):
    for book in all_books:
        if book.id == id:
            return book
    raise HTTPException(status_code=404, detail="The book not found")

@app.post('/books', response_model=Book)
def create_book(book:BookCreate):
    if not book:
        raise HTTPException(status_code=404, detail="The book not empty")
    all_books.append(book)
    return book

@app.put("/books/{id}")
def update_book(id:int, updated_book:BookUpdate):
    for i, book in enumerate(all_books):
        if book.id == id:
            _book = Book(**updated_book.model_dump(), id=id )
            all_books[i] = _book
            return _book
    raise HTTPException(status_code=404, detail="The book not found")