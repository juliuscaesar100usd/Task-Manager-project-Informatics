from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def get_db():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db)]

