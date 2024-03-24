from sqlalchemy import create_engine, Integer, String, DateTime, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker, mapped_column
from typing import Annotated
from datetime import datetime

import config

engine = create_engine(url=config.get_db_url())
Session = sessionmaker(bind=engine, autoflush=False)

pk = Annotated[int, mapped_column(primary_key=True, nullable=False, unique=True, autoincrement=True)]
str_256 = Annotated[str, 256]
dt = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]


class Base(DeclarativeBase):
    type_annotation_map = {
        pk: Integer,
        str_256: String(256),
        dt: DateTime,
    }


def create_tables():
    Base.metadata.create_all(engine)
