from aiozmq import rpc
from mas.daemon import Service
from mas.common import ADDRESS
from mas.lib import Worker

class Mas(object):
    
    def __init__(self, worker=None):
        self.service = None
        self.worker = worker
    
    async def start(self):
        self.server = await rpc.serve_rpc(Service(self.worker), bind=ADDRESS)
        await self.server.wait_closed()

    async def close(self):
        pass
