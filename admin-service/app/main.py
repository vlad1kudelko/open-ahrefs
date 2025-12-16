import uvicorn
from endpoints.crudtask import crudtask
from fastapi import FastAPI

app = FastAPI()

app.include_router(crudtask, prefix="/crudtask")


@app.get("/")
def index():
    return "Welcome to the 'open-ahrefs' project"


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", reload=True)
