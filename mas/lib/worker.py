class Worker(object):
    def __init__(self):
        self.notify = None

    async def request(self, theater, day, time, movie, seat, n, silent=True):
        pass

    async def terminate(self, worker_id):
        pass

    async def status(self):
        pass
