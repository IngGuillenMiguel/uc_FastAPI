from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, validator, Field, EmailStr, HttpUrl
# from pydantic import field_validator


class StatusType(str, Enum):
    DONE = 'done'
    PENDING = 'pending'


class IDFieldModel(BaseModel):
    # Field: Validación sencilla, si se ocupa algo mas complejo seria con validator
    id: int = Field(ge=1, le=10000000)

    @validator('id')
    def id_greater_than_Zero(cls, v):
        if v <= 0:
            raise ValueError('must be greater than zero')
        return v

    @validator('id')
    def id_less_than_than_thousand(cls, v):
        if v >= 1000:
            raise ValueError('must be less than thousand')
        return v


class Category(IDFieldModel):
    name: str


class User(IDFieldModel):
    name: str = Field(min_length=10, max_length=255)
    surname: str
    email: EmailStr
    website: HttpUrl


class Task(IDFieldModel):
    name: str
    description: Optional[str] = Field(None, min_length=10, max_length=255)
    status: StatusType
    category: Category
    user: User
    # tags: List[str] = []
    tags: set[str] = set()  # no permiti repetir elementos en una lista

    # @field_validator('name')
    @validator('name')
    def name_alphanumeric_and_whitespace(cls, v):
        if v.replace(" ", '').isalnum():
            return v
        raise ValueError('must be a alphanumeric')
