from sqlalchemy.orm import DeclarativeBase, MappedColumn, mapped_column
from sqlalchemy import Integer, DateTime, func
from typing import Annotated

# Anotaciones reutilizables entre tablas
intpk = Annotated[int, mapped_column(Integer, primary_key=True, autoincrement=True)]

class Base(DeclarativeBase):
    pass

class BaseModel(Base):
    __abstract__ = True

    id: MappedColumn[intpk]
    created_at = mapped_column(DateTime, server_default=func.now())
    updated_at = mapped_column(DateTime, onupdate=func.now())
