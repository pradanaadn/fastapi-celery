from contextlib import asynccontextmanager
from multiprocessing import Process

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from celery.result import AsyncResult
from background_celery_client import Task
import task


@asynccontextmanager
async def lifespan(app: FastAPI):
    Task.launch_worker()

    yield

    Task.stop_worker()


app = FastAPI(lifespan=lifespan)


class TaskOut(BaseModel):
    id: str
    status: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/start")
def start() -> TaskOut:
    r = task.dummy_task.delay()
    return _to_task_out(r)


@app.get("/status")
def status(task_id: str) -> TaskOut:
    r = Task.get_client().AsyncResult(task_id)
    return _to_task_out(r)


def _to_task_out(r: AsyncResult) -> TaskOut:
    return TaskOut(id=r.task_id, status=r.status)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
