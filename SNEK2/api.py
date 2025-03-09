class Arity:
    def __init__(self, min=0, max=None):
        self.min = min
        self.max = max

    def __eq__(self, value):
        if value < self.min:
            return False
        if self.max is None:
            return True
        if value > self.max:
            return False
        
    def __neq__(self, value):
        return not self.__eq__(value)
    
    def __str__(self):
        max = self.max
        if self.max is None:
            max = "inf"
        return f"arity (between {self.min} and {max})"

class SNEKCallable:
    def __init__(self, func, arity):
        self.func = func
        self._arity = arity

    async def call(self, interpreter, args):
        return self.func(*args)

    def arity(self):
        return self._arity


class AsyncSNEKCallable(SNEKCallable):
    async def call(self, interpreter, args):
        return await self.func(*args)
