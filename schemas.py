from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, validator, Field, EmailStr, HttpUrl
from fastapi import Form
# from pydantic import field_validator


class StatusType(str, Enum):
    DONE = 'done'
    PENDING = 'pending'


class Category(BaseModel):
    name: str


class User(BaseModel):
    name: str = Field(min_length=5, max_length=255)
    surname: str
    email: EmailStr
    website: HttpUrl


class Task(BaseModel):
    name: str
    description: Optional[str] = Field(None, min_length=10, max_length=255)
    status: StatusType
    # category: Category
    # user: User
    # tags: List[str] = []
    category_id: int
    user_id: int
    tags: set[str] = set()  # no permiti repetir elementos en una lista

    @classmethod
    def as_form(cls,
                name: str = Form(),
                description: str = Form(),
                status: str = Form(),
                category_id: str = Form(),
                user_id: str = Form(),
                ):
        return cls(name=name, description=description, status=status, category_id=category_id, user_id=user_id)

    class Config:
        # orm_mode = True
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 123,
                "name": "Primer tarea",
                "description": "Realizar la tarea asignada",
                "status": StatusType.PENDING,
                "tags": ["tag 1", "tag 2"],
                # "category": {
                #        "id": 123,
                #        "name": "category 1"
                # },
                # "user": {
                #    "id": 12,
                #    "name": "Luffy",
                #    "email": "luffy.monekyd@gmails.com",
                #    "surname": "D",
                #    "website": "https://reydelospiratas.com"
                # }
            }
        }

    # @field_validator('name')
    @validator('name')
    def name_alphanumeric_and_whitespace(cls, v):
        if v.replace(" ", '').isalnum():
            return v
        raise ValueError('must be a alphanumeric')


class TaskRead(Task):
    id: int


class TaskWrite(Task):
    id: Optional[int] = Field(default=None)
    user_id: Optional[int] = Field(default=None)

    @classmethod
    def as_form(cls,
                name: str = Form(),
                description: str = Form(),
                status: str = Form(),
                category_id: str = Form(),
                user_id: str = Form(),
                ):
        return cls(name=name, description=description, status=status, category_id=category_id, user_id=user_id)
