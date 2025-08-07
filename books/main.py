
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import IntEnum

app = FastAPI()

all_books= []

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
    id: int = Field(..., description='Unique identifier of the book')
    title: str = Field(..., min_length=1, max_length=512, description='Title of the book')
    author: str = Field(..., min_length=1, max_length=512, description='Author of the book')
    description: str = Field(..., min_length=1, max_length=1000, description='Description of the book')
    rating: int = Field(1,min_length=1, max_length=5 ,description='The rating of the book')

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=512, description='Title of the book')
    author: Optional[str] = Field(..., min_length=1, max_length=512, description='Author of the book')
    description: Optional[str] = Field(..., min_length=1, max_length=1000, description='Description of the book')
    rating: Optional[int] = Field(1, min_length=1, max_length=5, description='The rating of the book')

@app.get("/")
def index():
    return {'message': 'Hello Book Project'}

@app.get("/books")
def get_all_books():
    return all_books