from abc import ABC, abstractmethod
from typing import Sequence, Any


class Interpreter(ABC):
    ...


class Arity(ABC):
    @abstractmethod
    def __eq__(self, value: object) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __neq__(self, value: object) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError


class SNEKCallable(ABC):
    @abstractmethod
    async def call(self, interpreter: Interpreter, args: Sequence[Any]) -> Any:
        raise NotImplementedError

    @abstractmethod
    def arity(self) -> Arity:
        raise NotImplementedError