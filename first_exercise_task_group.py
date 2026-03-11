import asyncio
import random
from datetime import datetime


async def worker(x: int):
    print(f"start {x}")
    await asyncio.sleep(x)
    print(f"finish {x}")

async def main():
    start = datetime.now()
    async with asyncio.TaskGroup() as tg:
        tasks = [1, 2, 3]
        random.shuffle(tasks)
        for x in tasks:
            tg.create_task(worker(x))
    print(f"time elapsed: {datetime.now() - start}")

if __name__ == '__main__':
    print("start event loop")
    asyncio.run(main())
    print("finish event loop")

