from typing import Optional, List
from enum import IntEnum

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI()


class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class TodoBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=512, description='Name of the todo')
    description: str = Field(..., max_length=1000, description='Description of the todo')
    priority: Priority = Field(default=Priority.LOW, description='Priority of the todo')

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    id: int = Field(..., description='Unique identifier of todo')

class TodoUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=512, description='Name of the todo')
    description: Optional[str] = Field(None, max_length=1000, description='Description of the todo')
    priority: Optional[Priority] = Field(None, description='Priority of the todo')


_all_todos =[
    Todo(id=1, name='Sport', description='Go to the gym', priority=Priority.MEDIUM),
    Todo(id=2, name='Read2', description='Read 10 pages', priority=Priority.HIGH),
    Todo(id=3, name='Shop', description='Go shopping', priority=Priority.LOW),
    Todo(id=4, name='Study', description='Learn to exam', priority=Priority.MEDIUM),
    Todo(id=5, name='Meditate', description='Meditate 20 minutes', priority=Priority.HIGH),
]

#GET | POST | PUT | DELETE
@app.get('/')
def index():
    return {"message":"Hello word"}

@app.get('/todos/{id}', response_model=Todo)
def get_todo(id: int):
    for todo in _all_todos:
        if todo.id == id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.get('/todos', response_model= List[Todo])
def get_todos(first_n:int = None):
    if first_n:
        return _all_todos[:first_n]
    else:
        return _all_todos


@app.post('/todos', response_model=Todo)
def create_todo(todo: TodoCreate):
    new_id = max(todo.id for todo in _all_todos) + 1
    new_todo = Todo(id=new_id, name=todo.name, description=todo.description, priority=todo.priority)
    _all_todos.append(new_todo)
    return new_todo

# @app.put('/todos/{id}', response_model=Todo)
# def update_todo(id:int, updated_todo:TodoUpdate):
#     for todo in _all_todos:
#         if todo.id == id:
#             todo.name = updated_todo.name
#             todo.description = updated_todo.description
#             return  todo
#     return 'error: todo not found'

#-------advance--level 1
@app.put('/todos/{id}', response_model=Todo)
def update_todo(id:int, updated_todo:TodoUpdate):
    todo = next((td for td in _all_todos if td.id == id), None)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    updated_data = updated_todo.model_dump(exclude_unset=True)

    for field, value in updated_data.items():
        setattr(todo, field, value)
    return todo

# ---Cach 2
@app.patch('/todos/{id}', response_model=Todo)
def update_todo_partial(id:int, updated_todo:TodoUpdate):
    for i, todo in enumerate(_all_todos):
        if todo.id == id:
            updated_data = updated_todo.model_dump(exclude_unset=True)
            updated = todo.model_copy(update=updated_data)
            _all_todos[i] = updated
            return updated

    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete('/todos/{id}', response_model=Todo)
def delete_todo(id:int):
    for index, todo in enumerate(_all_todos):
        if todo.id == id:
            new_todos = _all_todos.pop(index)
            return new_todos

    raise HTTPException(status_code=404, detail="Todo not found")
@app.delete('/todos')
def delete_all():
    _all_todos.clear()
    return 'Success, deleted all'