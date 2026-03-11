import asyncio
from asyncio import sleep
from datetime import datetime
from random import uniform

class Task:
    last_tid: int = 0

    def __init__(self, time: float):
        self.time: float = time
        self.tid: int = Task.last_tid
        Task.last_tid += 1

    def __str__(self):
        return f"[tid: {self.tid}, time: {self.time}]"

tasks = asyncio.Queue()
MAX_TIME = 3
NUM_OF_TASKS = 5
TIME_START = datetime.now()
CREATION_DELAY = 2

def print_with_time(message):
    print(f"{datetime.now() - TIME_START}: {message}")

#The boring way
async def boring_worker():
    task = await tasks.get()
    if task.time > MAX_TIME:
        print_with_time(f"canceling task {task}")
        return
    print_with_time(f"starting task {task}")
    await sleep(task.time)
    print_with_time(f"finished task {task}")

#The cool way
async def cool_worker():
    task = await tasks.get()
    print_with_time(f"starting task {task}")
    try:
        async with asyncio.timeout(MAX_TIME) as tg:
            await sleep(task.time)
            print_with_time(f"ending task {task}")
    except asyncio.TimeoutError:
        print_with_time(f"Task {task} canceled")

async def producer(num_of_tasks: int):
    for i in range(num_of_tasks):
        await sleep(CREATION_DELAY)
        task = Task(uniform(1.0,4.0))
        print_with_time(f"putting task {task}")
        await tasks.put(task)

async def main():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(producer(NUM_OF_TASKS))
        for _ in range(NUM_OF_TASKS):
            tg.create_task(cool_worker())

if __name__ == '__main__':
    print_with_time("start event loop")
    asyncio.run(main())
    print("end event loop")
