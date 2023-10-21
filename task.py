from fastapi import APIRouter, Body, status, HTTPException
from models import Task

task_router = APIRouter(
    prefix="/task",
    tags=["task"])

task_list = []


@task_router.get('/', status_code=status.HTTP_200_OK)
def get():
    return {"task": task_list}


@task_router.post('/', status_code=status.HTTP_201_CREATED)
def add(task: Task):
    if task in task_list:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Task '+task.name+' already exists')
    task_list.append(task)
    return {"task": task_list}


@task_router.put('/', status_code=status.HTTP_200_OK)
def update(index: int, task: Task):
    # task_list[index] = {
    #    "task": task,
    #    "status": status
    # }
    if len(task_list) <= index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Task ID does not exists')
    return {"task": task_list}


@task_router.delete('/', status_code=status.HTTP_200_OK)
def delete(index: int):
    if len(task_list) <= index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Task ID does not exists')
    del task_list[index]
    return {"task": task_list}
