import asyncio, time

from SNEK2 import SNEKCallable, SNEKProgram

class test:
    def __str__(self):
        return "I'm a boogerface!!!!"

def main():
    with open("exp.snek") as f:
        source = f.read()
    
    program = SNEKProgram(source, {
        "barf": SNEKCallable(lambda: print("Eww, I just barfed!"), 0),
        "get_test": SNEKCallable(lambda: test(), 0),
    })
    asyncio.run(program.run())


if __name__ == "__main__":
    main()