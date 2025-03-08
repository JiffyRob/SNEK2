import asyncio, time

from SNEK2 import SNEKCallable, SNEKProgram

running = True


class test:
    def __str__(self):
        return "I'm a boogerface!!!!"


async def run_game():
    while running:
        print("new frame")
        await asyncio.sleep(0.1)


async def run_script():
    with open("exp.snek") as f:
        source = f.read()

    await SNEKProgram(
        source,
        {
            "barf": SNEKCallable(lambda: print("Eww, I just barfed!"), 0),
            "get_test": SNEKCallable(lambda: test(), 0),
        },
    ).run_async()
    global running
    running = False


async def main():
    asyncio.create_task(run_script())
    await run_game()


if __name__ == "__main__":
    asyncio.run(main())
