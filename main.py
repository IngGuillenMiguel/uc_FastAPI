from database.models import Task, Category
from database import crud
from database.database import Base, engine, get_database_session
from myupload import upload_router
from task import task_router
from fastapi import FastAPI, Depends, APIRouter, Query, Path, Request, Header, HTTPException, status
from fastapi.templating import Jinja2Templates
from typing import Optional
from sqlalchemy.orm import Session
from typing_extensions import Annotated

templates = Jinja2Templates(directory="templates/")

app = FastAPI()
router = APIRouter()

Base.metadata.create_all(bind=engine)


@router.get('/hello')
def hello_world():
    return {"hello": "world"}


@app.get('/e_page')
def page(page: int = Query(1, ge=0, le=20), size: int = Query(5, ge=5, le=20)):
    return {"page": page, "size": size}


@app.get("/e_phone/")
# def phone(phone: str = Path(pattern=r"^(\(?\+[\d]{1,3}\)?)\s?([\d]{1,5})\s?([\d][\s\.-]?){6,7}$")
def phone(phone: str = Query(regex=r"^(\(?\+[\d]{1,3}\)?)\s?([\d]{1,5})\s?([\d][\s\.-]?){6,7}$")):
    return {"phone": phone}


@app.get("/ep_phone/{phone}")
# def phone(phone: str = Path(pattern=r"^(\(?\+[\d]{1,3}\)?)\s?([\d]{1,5})\s?([\d][\s\.-]?){6,7}$")
def phone(phone: str = Path(pattern=r"^(\(?\+[\d]{1,3}\)?)\s?([\d]{1,5})\s?([\d][\s\.-]?){6,7}$", example="+52 646 123 45 67")):
    return {"phone": phone}


@app.get('/page')  # Templates
def index(request: Request, db: Session = Depends(get_database_session)):
    categories = db.query(Category).all()
    return templates.TemplateResponse('task/index.html', {"request": request, "tasks": crud.getAll(db), "categories": categories})

# Start.DEPENDS


def pagination(page: Optional[int] = 1, limit: Optional[int] = 10):
    return {'page': page, 'limit': limit}


@app.get('/p-task')
def index(pag: dict = Depends(pagination)):
    return pag

# PATH


def validate_token(token: str = Header()):
    if token != "TOKEN":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@app.get('/route-protected', dependencies=[Depends(validate_token)])
def protected_route(index: int):
    return {'hello': 'FastAPI'}


# VAR
CurrentTaskId = Annotated[int, Depends(validate_token)]


@app.get('/route-protected2')
def protected_route2(CurrentTaskId, index: int):
    return {'hello': 'FastAPI'}


@app.get('/route-protected3')
def protected_route3(CurrentTaskId, index: int, user_id: int):
    return {'hello': 'FastAPI'}

# Ends.DEPENDS


app.include_router(router)
app.include_router(task_router)
app.include_router(upload_router)
