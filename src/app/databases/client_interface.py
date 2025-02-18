from abc import ABC, abstractmethod
from typing import Any


class DBClientInterface(ABC):
    @abstractmethod
    def connect(self) -> Any:
        """Establish a connection to the database."""
        pass

    @abstractmethod
    def get_database(self) -> Any:
        """Return the database instance."""
        pass
