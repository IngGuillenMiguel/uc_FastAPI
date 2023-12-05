from fastapi import APIRouter, Body, Depends, Path, status, HTTPException
from sqlalchemy.orm import Session

from database.database import get_database_session
from schemas import Task, TaskRead, TaskWrite
from database import crud, models
from dataexample import taskWithORM

task_router = APIRouter(
    prefix="/task",
    tags=["task"])

task_list = []


@task_router.get('/all/TaskRead', status_code=status.HTTP_200_OK)
def get(db: Session = Depends(get_database_session)):
    return {"tasks": [TaskRead.from_orm(task) for task in crud.getAll(db)]}


@task_router.post('/post/TaskWrite', status_code=status.HTTP_201_CREATED)
def add(task: TaskWrite = Body(examples=taskWithORM), db: Session = Depends(get_database_session)):
    return {"tasks": TaskWrite.from_orm(crud.create(task, db=db))}


@task_router.put('/TaskWrite/{id}', status_code=status.HTTP_200_OK)
def update(id: int = Path(ge=1), task: TaskWrite = Body(examples=taskWithORM), db: Session = Depends(get_database_session)):
    return {"task": crud.update(id, task, db)}


@task_router.get('/pydantic/all', status_code=status.HTTP_200_OK)
def get(db: Session = Depends(get_database_session)):
    return {"task": [Task.from_orm(task) for task in crud.getAll(db)]}


@task_router.get('/pydantic/{id}', status_code=status.HTTP_200_OK)
def get(id: int = Path(ge=1), db: Session = Depends(get_database_session)):
    return Task.from_orm(crud.getByID(id, db))


@task_router.get('/relation_task_category', status_code=status.HTTP_200_OK)
def get(db: Session = Depends(get_database_session)):
    task = crud.getByID(db=db, id=1)
    print(task.category.name)
    return {"task": task}


@task_router.get('/relation_task_user', status_code=status.HTTP_200_OK)
def get(db: Session = Depends(get_database_session)):
    task = crud.getByID(db=db, id=1)
    print(task.user.name)
    return {"task": task}


@task_router.get('/relation_category_task', status_code=status.HTTP_200_OK)
def get(db: Session = Depends(get_database_session)):
    task = db.query(models.Category).get(1).tasks
    print(db.query(models.Category).get(1).tasks)
    return {"task": task}


@task_router.get('/relation_user_task', status_code=status.HTTP_200_OK)
def get(db: Session = Depends(get_database_session)):
    task = db.query(models.User).get(1).tasks
    print(db.query(models.User).get(1).tasks)
    return {"task": task}


@task_router.get('/paginate', status_code=status.HTTP_200_OK)
def get(db: Session = Depends(get_database_session)):
    print(crud.pagination(4, 5, db))
    return {"task": task_list}


@task_router.get('/all', status_code=status.HTTP_200_OK)
def get(db: Session = Depends(get_database_session)):
    tasks = crud.getAll(db)
    return {"task": tasks}


@task_router.get('/{id}', status_code=status.HTTP_200_OK)
def get(id: int = Path(ge=1), db: Session = Depends(get_database_session)):
    return crud.getByID(id, db)


@task_router.post('/form-create', status_code=status.HTTP_201_CREATED)
def addForm(task: TaskWrite = Depends(TaskWrite.as_form), db: Session = Depends(get_database_session)):
    return {"task": crud.create(task, db=db)}


@task_router.post('/', status_code=status.HTTP_201_CREATED)
def add(task: Task = Body(examples=taskWithORM), db: Session = Depends(get_database_session)):
    return {"task": crud.create(task, db=db)}


@task_router.put('/{id}', status_code=status.HTTP_200_OK)
def update(id: int = Path(ge=1), task: Task = Body(examples=taskWithORM), db: Session = Depends(get_database_session)):
    return {"task": crud.update(id, task, db)}


@task_router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete(id: int = Path(ge=1), db: Session = Depends(get_database_session)):
    crud.delete(id, db)
    return {"task": crud.getAll(db)}


@task_router.put('/tag/add/{id}', status_code=status.HTTP_200_OK)
def tagAdd(id: int = Path(ge=1), idTag: int = Body(ge=1), db: Session = Depends(get_database_session)):
    return crud.tagAdd(id, idTag, db)


@task_router.delete('/tag/remove/{id}', status_code=status.HTTP_200_OK)
def tagRemove(id: int = Path(ge=1), idTag: int = Body(ge=1), db: Session = Depends(get_database_session)):
    return crud.tagRemove(id, idTag, db)
