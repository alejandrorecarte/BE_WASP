from abc import ABC, abstractmethod
from typing import Any, Dict


class DBHandlerInterface(ABC):
    @abstractmethod
    def create(self, data: Dict[str, Any]) -> str:
        """Insert a document into the database."""
        pass

    @abstractmethod
    def get(self, query: Dict[str, Any]) -> Any:
        """Get a document from the database."""
        pass

    @abstractmethod
    def update(self, query: Dict[str, Any], update_data: Dict[str, Any]) -> int:
        """Update a document in the database."""
        pass

    @abstractmethod
    def delete(self, query: Dict[str, Any]) -> int:
        """Delete a document from the database."""
        pass
