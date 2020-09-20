import asyncio

from mas import Mas
from mas import Worker

class SimpleWorker(Worker):

    def __init__(self):
        super().__init__()

    async def request(self, session, theater, day, time, movie, seat, n, silent=True):
        pass

    async def terminate(self, worker_id):
        pass

    async def status(self):
        return 0

async def main():
    async with Mas(SimpleWorker()) as mas:
        await mas.start()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
