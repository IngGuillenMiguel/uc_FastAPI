from fastapi import FastAPI, APIRouter, Query, Path
from task import task_router

app = FastAPI()
router = APIRouter()


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


app.include_router(router)
app.include_router(task_router)
