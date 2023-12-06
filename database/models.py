from sqlalchemy import Table
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import String, Integer, Text, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.database import Base
from schemas import StatusType

task_tag = Table('uc_uctask_tag', Base.metadata,
                 Column('task_id', Integer, ForeignKey(
                     'uc_uctasks.id'), primary_key=True),
                 Column('tag_id', Integer, ForeignKey(
                     'uc_uctags.id'), primary_key=True)
                 )


class Task(Base):
    __tablename__ = "uc_uctasks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250))  # , unique=True)
    description = Column(Text)
    status = Column(Enum(StatusType))
    category_id = Column(Integer, ForeignKey('uc_uccategories.id'))
    user_id = Column(Integer, ForeignKey('uc_ucusers.id'))
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())
    category = relationship('Category', lazy='joined', back_populates='tasks')
    user = relationship('User', lazy='joined', back_populates='tasks')
    tags = relationship('Tag', secondary=task_tag, back_populates='tasks')
    # tags = relationship('Tag', secondary=task_tag, backref='tasks') # al usar esto se omite en la otra tabla


class Category(Base):
    __tablename__ = "uc_uccategories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250))
    tasks = relationship('Task', back_populates='category', lazy='joined')


class User(Base):
    __tablename__ = "uc_ucusers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250))
    lastname = Column(String(250))
    email = Column(String(250))
    website = Column(String(250))
    hashed_password = Column(String(255))
    tasks = relationship('Task', back_populates='user', lazy='joined')


class Tag(Base):
    __tablename__ = "uc_uctags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250))
    tasks = relationship('Task', secondary=task_tag)


class AccessToken(Base):
    __tablename__ = "uc_ucaccess_token"
    user_id = Column(Integer, ForeignKey('uc_ucusers.id'), primary_key=True)
    access_token = Column(String(255))
    expiration_date = Column(DateTime(timezone=True))
    user = relationship('User', lazy='joined')
