from datetime import timedelta
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base, pk, str_256, dt


class Genre(Base):
    __tablename__ = "genre"

    id: Mapped[pk]
    name: Mapped[str_256]

    books: Mapped[list["Book"]] = relationship(back_populates="genre")


class Author(Base):
    __tablename__ = "author"

    id: Mapped[pk]
    name: Mapped[str_256]

    books: Mapped[list["Book"]] = relationship(back_populates="author")


class Book(Base):
    __tablename__ = "book"

    id: Mapped[pk]
    name: Mapped[str_256]
    price: Mapped[int]
    stock: Mapped[int]
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id", ondelete="CASCADE"))
    genre_id: Mapped[int] = mapped_column(ForeignKey("genre.id", ondelete="CASCADE"))

    author: Mapped["Author"] = relationship(back_populates="books")
    genre: Mapped["Genre"] = relationship(back_populates="books")
    buys: Mapped[list["Buy"]] = relationship(back_populates="books",
                                             secondary="buy_book",
                                             passive_deletes=True)


class City(Base):
    __tablename__ = "city"

    id: Mapped[pk]
    name: Mapped[str_256]
    delivery_time: Mapped[timedelta]

    clients: Mapped[list["Client"]] = relationship(back_populates="city")


class Client(Base):
    __tablename__ = "client"

    id: Mapped[pk]
    name: Mapped[str_256]
    email: Mapped[str_256]
    city_id: Mapped[int] = mapped_column(ForeignKey("city.id", ondelete="CASCADE"))

    buys: Mapped[list["Buy"]] = relationship(back_populates="buy")
    city: Mapped["City"] = relationship(back_populates="clients")


class Buy(Base):
    __tablename__ = "buy"

    id: Mapped[pk]
    wishes: Mapped[str]
    client_id: Mapped[int] = mapped_column(ForeignKey("client.id", ondelete="CASCADE"))

    books: Mapped[list["Book"]] = relationship(back_populates="buys",
                                               secondary="buy_book",
                                               cascade="all, delete")
    buy_step: Mapped["BuyStep"] = relationship(back_populates="buy")
    client: Mapped["Client"] = relationship(back_populates="buys")


class BuyBook(Base):
    __tablename__ = "buy_book"

    buy_id: Mapped[int] = mapped_column(ForeignKey("buy.id", ondelete="CASCADE"),
                                        primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id", ondelete="CASCADE"),
                                         primary_key=True)


class Step(Base):
    __tablename__ = "step"

    id: Mapped[pk]
    description: Mapped[str]
    buy_step_id: Mapped[int] = mapped_column(ForeignKey("buy_step.id", ondelete="CASCADE"))

    buy_step: Mapped["BuyStep"] = relationship(back_populates="steps")


class BuyStep(Base):
    __tablename__ = "buy_step"

    id: Mapped[pk]
    start: Mapped[dt]
    end: Mapped[dt]
    buy_id: Mapped[int] = mapped_column(ForeignKey("buy.id", ondelete="CASCADE"))

    steps: Mapped[list["Step"]] = relationship(back_populates="buy_step")
    buy: Mapped["Buy"] = relationship(back_populates="buy_step")
