from fastapi import FastAPI

app = FastAPI()

#GET | POST | PUT | DELETE
@app.get('/')
def index():
    return {"message":"Hello word"}