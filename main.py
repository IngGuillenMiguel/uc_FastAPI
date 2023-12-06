from database.models import Task, Category
from database import crud
from database.database import Base, engine, get_database_session
from myupload import upload_router
from task import task_router
from fastapi import FastAPI, Depends, APIRouter, Query, Path, Request, Header, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.security import APIKeyHeader
from typing import Optional
from sqlalchemy.orm import Session
from typing_extensions import Annotated
import time
from user import user_router
from authentication.authentication import verify_access_token

templates = Jinja2Templates(directory="templates/")

app = FastAPI()
router = APIRouter()

Base.metadata.create_all(bind=engine)

# start.middlewares


@app.middleware("http")
async def add_process_time_to_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    print("process_time")
    print(process_time)
    return response

# ends.middlewares

# Start.Token Auth
''' # TOKEN SIN DB
API_KEY_TOKEN_PASS = "SECRET_PASSWORD"
api_key_token = APIKeyHeader(name='Token')
@app.get("/protected-route")
def protected_route(token: str = Depends(api_key_token)):
    if token != API_KEY_TOKEN_PASS:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return {'hola': 'fastapi'}
'''
'''
# TOKEN CON DB
api_key_token = APIKeyHeader(name='Token')
@app.get("/protected-route")
def protected_route(token: str = Depends(api_key_token), db: Session = Depends(get_database_session)):
    user = db.query(User).join(AccessToken).filter(
        AccessToken.access_token == token).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return {'hola': 'fastapi'}
'''
# Ends.Token Auth

'''
@router.get('/hello', dependencies=[Depends(verify_access_token)])
def hello_world():
    return {"hello": "world"}
'''


@router.get('/hello')
def hello_world(user=Depends(verify_access_token), db: Session = Depends(get_database_session)):
    print('*******')
    print(user.name)
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
def route_protected(index: int):
    return {'hello': 'FastAPI'}


# VAR
CurrentTaskId = Annotated[int, Depends(validate_token)]


@app.get('/route-protected2')
def route_protected2(CurrentTaskId, index: int):
    return {'hello': 'FastAPI'}


@app.get('/route-protected3')
def route_protected3(CurrentTaskId, index: int, user_id: int):
    return {'hello': 'FastAPI'}

# Ends.DEPENDS


app.include_router(router)
app.include_router(task_router)
app.include_router(user_router)
app.include_router(upload_router)
