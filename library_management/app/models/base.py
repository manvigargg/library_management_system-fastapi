from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
import uuid

class BaseEntity(ABC):
    """Abstract base class for all entities"""
    
    def __init__(self, name: str):
        self._id: str = str(uuid.uuid4())
        self._name: str = name
        self._created_at: datetime = datetime.now()
        self._updated_at: datetime = datetime.now()
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str):
        if not value or not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value.strip()
        self._updated_at = datetime.now()
    
    @abstractmethod
    def to_dict(self) -> dict:
        """Convert object to dictionary representation"""
        pass
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, name={self.name})"