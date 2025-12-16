import asyncio
from contextlib import asynccontextmanager

import uvicorn
from background.task import pipe_push_while
from endpoints.crudtask import crudtask
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(pipe_push_while())
    yield
    task.cancel()


app = FastAPI(lifespan=lifespan)
app.include_router(crudtask, prefix="/crudtask")


@app.get("/")
def index():
    return "Welcome to the 'open-ahrefs' project"


if __name__ == "__main__":
    uvicorn.run("main:app")
