from app.endpoints.crudtask import crudtask
from fastapi import FastAPI

app = FastAPI()

app.include_router(crudtask, prefix="/crudtask")


@app.get("/")
def index():
    return "Welcome to the 'open-ahrefs' project"
