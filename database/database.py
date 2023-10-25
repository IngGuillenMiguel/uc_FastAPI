from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "mysql+pymysql://root:root@192.168.61.128:3306/mq_v11"

engine = create_engine(DATABASE_URL)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_database_session():  # Sirve para cerrar la sesion de cada usuario, una vez haya "terminado de usar la app"
    try:
        db = Session()
        yield db
    finally:
        db.close()
