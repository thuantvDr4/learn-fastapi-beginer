from fastapi import FastAPI

app = FastAPI()

all_todos =[
    {"id": 1, "name": "Sport", "description":"Go to the gym" },
    {"id": 2, "name": "Read", "description":"Read 10 pages" },
    {"id": 3, "name": "Shop", "description":"Go shopping" },
    {"id": 4, "name": "Study", "description":"Learn to exam" },
    {"id": 5, "name": "Meditate", "description":"Meditate 20 minutes" },
]

#GET | POST | PUT | DELETE
@app.get('/')
def index():
    return {"message":"Hello word"}

@app.get('/todos/{id}')
def get_todo(id: int):
    for todo in all_todos:
        if todo['id'] == id:
            return todo

@app.get('/todos')
def get_todos(first_n:int = None):
    if first_n:
        return all_todos[:first_n]
    else:
        return all_todos


@app.post('/todos')
def create_todo(todo: dict):
    new_id = max(todo['id'] for todo in all_todos) + 1
    new_todo ={
        "id": new_id,
        "name": todo['name'],
        "description": todo["description"]
    }
    all_todos.append(new_todo)
    return new_todo

@app.put('/todos/{id}')
def update_todo(id:int, updated_todo:dict):
    for todo in all_todos:
        if todo['id'] == id:
            todo['name'] = updated_todo['name']
            todo['description'] = updated_todo['description']
            return  todo
    return 'error: todo not found'

@app.delete('/todos/{id}')
def delete_todo(id:int):
    for index, todo in enumerate(all_todos):
        if todo['id'] == id:
            new_todos = all_todos.pop(index)
            return new_todos
    return 'Error, todo not found'

@app.delete('/todos')
def delete_all():
    all_todos.clear()
    return 'Success, deleted all'