from structlog import get_logger
import logging

log = get_logger()

class Worker(object):

    def __init__(self, ident, worker, notifier):
        self.ident = ident
        self.worker = worker

    async def request(self, theater, day, time, movie, seat, n, silent=True):
        if self.worker : await self.worker.request(theater, day, time, movie, seat, n, silent)
        log.info("request is activated")

    async def terminate(self, worker_id):
        if self.worker : await self.worker.terminate(worker_id)
        log.info("termination is activated")

    async def status(self):
        if self.worker : await self.worker.status()
        log.info("status is activated")
        return 0

    async def notity(self, msg):
        if self.worker : await self.worker.notify(msg)
        log.info("notity is activated")
