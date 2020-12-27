import asyncio
import copy
import os

from aiozmq import rpc
from structlog import get_logger

from mas.common import NUM_OF_WORKERS
from mas.daemon.worker import Worker
from mas.lib import Client

log = get_logger()


class Service(rpc.AttrHandler):
    def __init__(self, worker):
        self.worker = worker
        self.act_pool = set()
        self.inact_pool = set()
        self.listeners = []
        for ident in range(0, NUM_OF_WORKERS):
            worker = Worker(ident, copy.deepcopy(self.worker), self.notify)
            self.inact_pool.add(worker)

    async def notify(self, result):
        log.info(self.listeners)
        for listener in self.listeners:
            await listener.notify.notify(result)

    @rpc.method
    async def disconnect(self):
        log.info('disconnected successfully')

    @rpc.method
    async def subscribe(self, listener_addr):
        notifier = await rpc.connect_pipeline(connect=listener_addr)
        self.listeners.append(notifier)

    @rpc.method
    async def request(self, *args, **kwargs):
        log.debug("", args=args, kwargs=kwargs)

        if len(self.inact_pool) == 0:
            log.error('not enough worker', num_of_workers=NUM_OF_WORKERS)
            return -1

        worker = self.inact_pool.pop()
        ret = await worker.request(*args, **kwargs)

        self.act_pool.add(worker)
        log.info(
            'reservation started successfully', worker=worker.ident, ret=ret
        )

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
            ret = await hit.terminate(worker_id)
            self.inact_pool.add(hit)
            self.act_pool.remove(hit)
            log.info(
                f'terminate worker successfully', worker=worker_id, ret=ret
            )
        else:
            log.error('no such of worker')

        return ret

    @rpc.method
    async def status(self):
        log.debug("")
        ret = {}
        workers = list(self.act_pool)
        for worker in workers:
            ret[str(worker.ident)] = await worker.status()

        return ret
