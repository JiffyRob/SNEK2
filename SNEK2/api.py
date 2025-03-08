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
