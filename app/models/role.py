from sqlalchemy import Column, Integer, String
from app.database import Base
from app.models.base import BaseModelWithTimestamps

class Role(Base, BaseModelWithTimestamps):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
