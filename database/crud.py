from fastapi import HTTPException, status
from sqlalchemy.orm import Session, load_only
from database import models
from schemas import Task
from database.pagination import paginate, PageParams


def getAll(db: Session):

    task = db.query(models.Task).get(2)
    tag1 = db.query(models.Tag).get(1)

    # relacion muchos a muchos
    # task.tags.append(tag1)
    # db.add(tag1)
    # db.commit()
    # print(task.tags[0].name)

    # relacion "inversa" muchos a muchos
    # tag1.tasks.append(task)
    # db.add(tag1)
    # db.commit()

    task = db.query(models.Task).all()
    return task


def getByID(id: int, db: Session):
    # task = db.query(models.Task).filter(models.Task.id == id).first()
    task = db.query(models.Task).options(
        load_only(models.Task.name, models.Task.status)).get(id)
    # task = db.query(models.Task).get(id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return task


def create(task: Task, db: Session):
    taskdb = models.Task(
        name=task.name, description=task.description, status=task.status, category_id=task.category_id, user_id=task.user_id)
    db.add(taskdb)
    db.commit()
    db.refresh(taskdb)
    return taskdb


def update(id: int, task: Task, db: Session):
    taskdb = getByID(id, db)
    taskdb.name = task.name
    taskdb.description = task.description
    taskdb.status = task.status
    taskdb.category_id = task.category_id
    db.add(taskdb)
    db.commit()
    db.refresh(taskdb)
    return taskdb


def delete(id: int, db: Session):
    taskdb = getByID(id, db)
    db.delete(taskdb)
    db.commit()
    return taskdb


def pagination(page: int, size: int, db: Session):
    pageParams = PageParams()
    return paginate(pageParams, db.query(models.Task), Task)


def getTagById(id: int, db: Session):
    tag = db.query(models.Tag).get(id)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return tag


def tagAdd(id: int, idTag: int, db: Session):
    task = getByID(id, db)
    tag = getTagById(idTag, db)
    task.tags.append(tag)
    db.add(task)
    db.commit
    return task


def tagRemove(id: int, idTag: int, db: Session):
    task = getByID(id, db)
    tag = getTagById(idTag, db)
    task.tags.remove(tag)
    db.add(task)
    db.commit
    return task
