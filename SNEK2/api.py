from typing import Callable, Any, Sequence

from . import interfaces


class Arity(interfaces.Arity):
    def __init__(self, min: int=0, max: int | None=None) -> None:
        self.min = min
        self.max = max

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, int):
            return False
        if value < self.min:
            return False
        if self.max is None:
            return True
        if value > self.max:
            return False
        return True
        
    def __neq__(self, value: object) -> bool:
        return not self.__eq__(value)
    
    def __str__(self) -> str:
        max = self.max
        if self.max is None:
            return f"arity (between {self.min} and inf)"
        return f"arity (between {self.min} and {max})"
    
    def __repr__(self) -> str:
        return str(self)


class SNEKCallable:
    def __init__(self, func: Callable[..., Any], arity: int | Arity):
        self.func = func
        self._arity = arity

    async def call(self, interpreter: interfaces.Interpreter, args: Sequence[Any]) -> Any:
        return self.func(*args)

    def arity(self) -> int | interfaces.Arity:
        return self._arity


class AsyncSNEKCallable(SNEKCallable):
    async def call(self, interpreter: interfaces.Interpreter, args: Sequence[Any]) -> Any:
        return await self.func(*args)
