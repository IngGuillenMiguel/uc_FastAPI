from fastapi import APIRouter, File, UploadFile
from typing import List
import shutil

upload_router = APIRouter(
    prefix="/upload",
    tags=["upload"])


@upload_router.post('/file')
def upload_file(file: bytes = File()):
    return {"file_size": len(file)}


@upload_router.post('/upload_file_1')
def upload_upload_file_1(file: UploadFile):
    return {
        "file_name": file.filename,
        "content_type": file.content_type,
    }


@upload_router.post('/upload_file_2')
def upload_upload_file_2(file: UploadFile):
    with open("img/image.png", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {
        "file_name": file.filename,
        "content_type": file.content_type,
    }


@upload_router.post('/upload_file_3')
def upload_upload_file_3(images: List[UploadFile] = File()):
    for image in images:
        with open("img/i"+image.filename, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
