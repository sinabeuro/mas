class Worker(object):
    def __init__(self):
        self.notify = None

    async def request(self, *args, **kwargs):
        pass

    async def terminate(self, worker_id):
        pass

    async def status(self):
        pass
