from structlog import get_logger
import logging

log = get_logger()

class Worker(object):

    def __init__(self, ident, worker, notifier):
        self.ident = ident
        self.worker = worker
        self.notifier = notifier
        self.worker.notify = self.notify

    async def request(self, theater, day, time, movie, seat, n, silent=True):
        if self.worker : await self.worker.request(theater, day, time, movie, seat, n, silent)
        log.debug("request is activated")

    async def terminate(self, worker_id):
        if self.worker : await self.worker.terminate(worker_id)
        log.debug("termination is activated")

    async def status(self):
        if self.worker : await self.worker.status()
        log.debug("status is activated")
        return 0

    async def notify(self, msg):
        await self.notifier(msg)
        log.debug("notity is activated")
