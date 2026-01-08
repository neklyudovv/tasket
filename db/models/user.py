from . import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .task import Task


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    tasks = relationship("Task", back_populates="owner")
