from structlog import get_logger
import logging

log = get_logger()

class Worker(object):

    def __init__(self, ident, worker, notifier):
        self.ident = ident
        self.worker = worker
        
    async def request_reservation(self, theater, day, time, movie, seat, n, silent=True):
        if self.worker : self.worker.request_reservation(theater, day, time, movie, seat, n, silent)
        log.info("request is activated")

    async def terminate_reservation(self, worker_id):
        if self.worker : self.worker.terminate_reservation(worker_id)
        log.info("termination is activated")

    async def get_status(self):
        if self.worker : self.worker.get_status()
        log.info("get_status is activated")
        return 0

    async def notity(self, msg):
        if self.worker : self.worker.notify(msg)
        log.info("notity is activated")