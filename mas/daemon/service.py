import asyncio
from aiozmq import rpc
import os
import copy
from structlog import get_logger

from mas.common import NUM_OF_WORKERS
from mas.lib import Client
from mas.daemon import Worker

log = get_logger()

class Service(rpc.AttrHandler):

    def __init__(self, worker):
        self.worker = worker
        self.act_pool = set()
        self.inact_pool = set()
        self.listeners = []
        for ident in range(0, NUM_OF_WORKERS):
            worker = Worker(ident, copy.deepcopy(self.worker), self.on_noti_test)
            self.inact_pool.add(worker)

    async def on_noti_test(self, result):
        log.info(self.listeners)
        for listener in self.listeners:
            await listener.notify.on_noti_test(result)

    @rpc.method
    async def disconnect(self):
        pass

    @rpc.method
    async def pass_noti_pipeline(self, listener_addr):
        notifier = await rpc.connect_pipeline(connect=listener_addr)
        self.listeners.append(notifier)

    @rpc.method
    async def request(self, *args, **kwargs):
        log.debug("", args=args, kwargs=kwargs)

        if len(self.inact_pool) == 0:
            log.error("not enough worker", num_of_workers=NUM_OF_WORKERS)
            return -1

        worker = self.inact_pool.pop()
        ret = await worker.request(*args, **kwargs)

        self.act_pool.add(worker)
        log.info("reservation started successfully", worker=worker.ident)

        return worker.ident

    @rpc.method
    async def terminate(self, worker_id):
        hit = None
        ret = -1
        workers = list(self.act_pool)
        for worker in workers:
            if worker.ident == worker_id:
                hit = worker
                break

        if hit is not None:
            ret = await worker.terminate(worker_id)
            self.inact_pool.add(hit)
            self.act_pool.remove(worker)
            log.info("terminate worker successfully", worker=ret)
        else:
            log.error("no such of worker")

        return ret

    @rpc.method
    async def status(self):
        log.debug("")
        ret = {}
        workers = list(self.act_pool)
        for worker in workers:
            ret[str(worker.ident)] = await worker.status()

        return ret
