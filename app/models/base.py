from sqlalchemy import Column, DateTime, Integer, func
from sqlalchemy.ext.declarative import declared_attr

class BaseModelWithTimestamps:
    @declared_attr
    def created_at(cls):
        return Column(DateTime(timezone=True), server_default=func.now())
    
    @declared_attr
    def updated_at(cls):
        return Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    @declared_attr
    def created_by(cls):
        return Column(Integer, nullable=True)
    
    @declared_attr
    def updated_by(cls):
        return Column(Integer, nullable=True)
    
    @declared_attr
    def deleted_at(cls):
        return Column(DateTime(timezone=True), nullable=True)
    
    @declared_attr
    def deleted_by(cls):
        return Column(Integer, nullable=True)