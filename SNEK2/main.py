import asyncio
from functools import lru_cache

from .scan import Scanner
from .parse import Parser
from .interpret import Interpreter


class SNEKProgram:
    def __init__(self, script,  api=None):
        self.api = api
        if api is None:
            self.api = {}
        self.program = self._scan_and_parse(script)
        
    @lru_cache
    def _scan_and_parse(self, src):
        scanner = Scanner(src)
        return tuple(Parser(scanner.scan()).parse())

    def run(self):
        asyncio.run(Interpreter(self.api).interpret(self.program))

    async def run_async(self):
        await Interpreter(self.api).interpret(self.program)
