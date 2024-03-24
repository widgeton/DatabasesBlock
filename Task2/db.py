from sqlalchemy import create_engine, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase, sessionmaker, mapped_column
from typing import Annotated
from datetime import datetime, UTC

import config

engine = create_engine(url=config.DB_URL)
Session = sessionmaker(bind=engine, autoflush=False)

pk = Annotated[int, mapped_column(primary_key=True, nullable=False, unique=True, autoincrement=True)]
dt = Annotated[datetime, mapped_column(default=lambda: datetime.now(UTC))]


class Base(DeclarativeBase):
    type_annotation_map = {
        pk: Integer,
        dt: DateTime,
    }


def create_tables():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
