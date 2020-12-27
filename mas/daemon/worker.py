import logging

from arsenic import browsers, start_session
from arsenic.browsers import Firefox
from arsenic.services import Geckodriver
from structlog import get_logger

log = get_logger()


class Worker(object):
    def __init__(self, ident, worker, notifier, silent):
        self.ident = ident
        self.worker = worker
        self.notifier = notifier
        self.worker.notify = self.notify
        self.silent = silent
        self.browser = None
        self.session = None

    async def request(self, *args, **kwargs):
        if self.silent:
            self.browser = browsers.Firefox(
                **{'moz:firefoxOptions': {'args': ['-headless']}}
            )
        else:
            self.browser = Firefox()

        self.session = await start_session(Geckodriver(), self.browser)

        if self.worker:
            await self.worker.request(self.session, *args, **kwargs)
        log.debug('request is activated')
        return 0

    async def terminate(self, worker_id):
        if self.worker:
            await self.worker.terminate(worker_id)

        await self.session.close()
        log.debug('termination is activated')

    async def status(self):
        if self.worker:
            await self.worker.status()
        log.debug('status is activated')
        return 0

    async def notify(self, msg):
        await self.notifier(msg)
        log.debug('notity is activated')
