import asyncio
import json

import zmq
from aiozmq import rpc

from mas.common import ADDRESS


class NotifyHandler(rpc.AttrHandler):
    def __init__(self, notify=None, on_reserved=None):
        self.notify_cb = notify

    @rpc.method
    async def notify(self, result):
        if self.notify_cb is not None:
            await self.notify_cb(result)


class Client:
    def __init__(self):
        self.client = None
        self.ident = None
        self.listener = None

    async def connect(self, connect=ADDRESS, notify=None, on_reserved=None):
        self.client = await rpc.connect_rpc(connect=connect, timeout=1)
        self.client.transport.setsockopt(zmq.LINGER, 0)
        self.listener = await rpc.serve_pipeline(
            NotifyHandler(notify=notify), bind='ipc://*:*'
        )
        listener_addr = list(self.listener.transport.bindings())[0]
        await self.client.call.subscribe(listener_addr)

        return self.client

    async def disconnect(self):
        self.listener.close()
        await self.client.call.disconnect()
        self.client.close()

    async def request(self, theater, day, time, movie, seat, n, silent):
        silent = json.loads(silent.lower())
        self.ident = await self.client.call.request(
            theater, day, time, movie, seat, n, silent
        )
        return self.ident

    async def terminate(self, worker_id):
        ret = await self.client.call.terminate(worker_id)
        return ret

    async def status(self):
        ret = await self.client.call.status()
        return ret
