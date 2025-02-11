from abc import ABC, abstractmethod
from collections.abc import Container

class Nullable(ABC):
    @abstractmethod
    def __null__(self):
        pass

class Appendable(Container, ABC):
    @abstractmethod
    def __append__(self):
        pass
