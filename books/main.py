
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import IntEnum

app = FastAPI()

class Book:
    id: int
    title: str
    author:str
    description: str
    rating: int
    def __init__(self,id, title, author, description, rating):
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.id = id

class BookBase(BaseModel):
    # id: int = Field(..., description='Unique identifier of the book')
    title: str = Field(..., min_length=1, max_length=512, description='Title of the book')
    author: str = Field(..., min_length=1, max_length=512, description='Author of the book')
    description: str = Field(..., min_length=1, max_length=1000, description='Description of the book')
    rating: int = Field(gt=0, lt=5,description='The rating of the book')

class BookRes(BookBase):
    id: int = Field(..., description='Unique identifier of book')

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=512, description='Title of the book')
    author: Optional[str] = Field(..., min_length=1, max_length=512, description='Author of the book')
    description: Optional[str] = Field(..., min_length=1, max_length=1000, description='Description of the book')
    rating: Optional[int] = Field(gt=0, lt=5,description='The rating of the book')


all_books = [
    Book(id=1, title='Todo1', author='Todo1', description='Todo1 description', rating=1),
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

@app.get("/books/{id}", response_model = BookRes)
def get_book(id:int):
    for book in all_books:
        if book.id == id:
            return book
    raise HTTPException(status_code=404, detail="The book not found")

@app.post('/books', response_model=BookRes)
def create_book(book:BookCreate):
    if not book:
        raise HTTPException(status_code=404, detail="The book not empty")
    new_id = max(bk.id for bk in all_books) + 1

    new_book = Book(**book.model_dump(), id=new_id, )
    all_books.append(new_book)
    return new_book