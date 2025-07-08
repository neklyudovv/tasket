from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .task import Task
from .user import User