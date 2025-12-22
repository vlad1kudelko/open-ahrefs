import asyncio
from contextlib import asynccontextmanager

import uvicorn
from background.pipe_pull import pipe_pull_while
from background.pipe_push import pipe_push_while
from endpoints.crudtask import crudtask
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator


@asynccontextmanager
async def lifespan(app: FastAPI):
    task_push = asyncio.create_task(pipe_push_while())
    task_pull = asyncio.create_task(pipe_pull_while())
    yield
    task_push.cancel()
    task_pull.cancel()


app = FastAPI(lifespan=lifespan)
app.include_router(crudtask, prefix="/crudtask")
Instrumentator().instrument(app).expose(app)


@app.get("/")
def index():
    return "Welcome to the 'open-ahrefs' project"


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0")
