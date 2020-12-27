import asyncio
import signal

from aiozmq import rpc
from structlog import get_logger

from mas.common import ADDRESS
from mas.daemon import Service
from mas.lib import Worker

log = get_logger()


class Mas(object):
    def __init__(self, worker=None, silent=True):
        self.service = None
        self.worker = worker
        self.service = Service(self.worker)
        self.started = False
        signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
        for s in signals:
            asyncio.get_event_loop().add_signal_handler(
                s, lambda s=s: asyncio.create_task(self.shutdown(s))
            )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            log.exception(exc_value)
        await self.close()

    async def shutdown(self, signal):
        log.info(f'Received signal {signal.name}...')
        tasks = [
            t for t in asyncio.all_tasks() if t is not asyncio.current_task()
        ]
        [task.cancel() for task in tasks]

    async def start(self):
        self.server = await rpc.serve_rpc(self.service, bind=ADDRESS)
        self.started = True
        try:
            await self.server.wait_closed()
        except asyncio.CancelledError:
            log.info('cancelled service')
        finally:
            await self.close()

    async def close(self):
        if self.started:
            await self.service.notify(-1)
            self.started = False
