from aiozmq import rpc

from structlog import get_logger

from mas.daemon import Service
from mas.common import ADDRESS
from mas.lib import Worker

log = get_logger()

class Mas(object):

    def __init__(self, worker=None):
        self.service = None
        self.worker = worker

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            log.exception(exc_value)
        self.close()

    async def start(self):
        self.server = await rpc.serve_rpc(Service(self.worker), bind=ADDRESS)
        await self.server.wait_closed()

    async def close(self):
        pass
