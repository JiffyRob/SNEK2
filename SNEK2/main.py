import asyncio
from functools import lru_cache
from typing import Any

from .scan import Scanner
from .parse import Parser
from .interpret import Interpreter

from . import interfaces

class SNEKProgram(interfaces.Interpreter):
    def __init__(self, script: str, api: dict[str, Any] | None=None):
        self.api = api
        if api is None:
            self.api = {}
        self.program = self._scan_and_parse(script)
        # NOTE: The innards of SNEK are super dynamic and too annoying to type hint
        # NOTE: Hence, this file is full of type: ignore directives!

    @lru_cache
    def _scan_and_parse(self, src):  # type: ignore
        scanner = Scanner(src)  # type: ignore
        return tuple(Parser(scanner.scan()).parse())  # type: ignore

    def run(self) -> None:
        asyncio.run(Interpreter(self.api).interpret(self.program))  # type: ignore

    async def run_async(self) -> None:
        await Interpreter(self.api).interpret(self.program)  # type: ignore
