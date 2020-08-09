class Worker(object):
        
    async def request_reservation(self, theater, day, time, movie, seat, n, silent=True):
        pass

    async def terminate_reservation(self, worker_id):
        pass

    async def get_status(self):
        pass

    async def notity(self, msg):
        pass
