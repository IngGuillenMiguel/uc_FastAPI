from fastapi import APIRouter, Body
from models import Task

task_router = APIRouter(
    prefix="/task",
    tags=["task"])

task_list = [
    {
        'task': 'task',
        'status': 'done'
    }
]


@task_router.get('/')
def get():
    return {"task": task_list}


@task_router.post('/')
def add(task: Task):
    task_list.append(task)
    return {"task": task_list}


@task_router.put('/')
def update(index: int, task: Task):
    # task_list[index] = {
    #    "task": task,
    #    "status": status
    # }
    return {"task": task_list}


@task_router.delete('/')
def delete(index: int):
    del task_list[index]
    return {"task": task_list}
