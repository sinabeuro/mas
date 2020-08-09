import asyncio

from mas import Mas
from mas import Worker

class SimpleWorker(Worker):

    def __init__(self):
        super().__init__()

    async def request_reservation(self, theater, day, time, movie, seat, n, silent=True):
        pass

    async def terminate_reservation(self, worker_id):
        pass

    async def get_status(self):
        return 0

    async def notity(self, msg):
        pass

async def main():
    mas = Mas(SimpleWorker())
    await mas.start()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())