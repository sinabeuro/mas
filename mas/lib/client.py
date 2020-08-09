import asyncio
from aiozmq import rpc
from mas.common import ADDRESS

class NotifyHandler(rpc.AttrHandler):

    def __init__(self, notify= None, on_reserved=None):
        self.on_noti_test_cb = notify
        self.on_reserved_cb = on_reserved

    @rpc.method
    async def notify(self, result):
        if self.on_noti_test_cb is not None:
            await self.on_noti_test_cb(result)

    @rpc.method
    async def on_reserved(self, result):
        if self.on_reserved_cb is not None:
            await self.on_reserved_cb(result)

class Client():
    def __init__(self):
        self.client = None
        self.ident = None
        self.listener = None

    async def connect(self, connect=ADDRESS, notify=None, on_reserved=None):
        self.client = await rpc.connect_rpc(connect=connect, timeout=10)
        self.listener = await rpc.serve_pipeline(NotifyHandler(notify=notify), bind='ipc://*:*')
        listener_addr = list(self.listener.transport.bindings())[0]
        await self.client.call.pass_noti_pipeline(listener_addr)

        return self.client

    async def disconnect(self):
        await self.listener.close()
        await self.client.call.disconnect()

    async def request_reservation(self, theater, day, time, movie, seat, n, silent="True"):
        self.ident = await self.client.call.request_reservation(theater,
            day, time, movie, seat, n, silent)
        return self.ident

    async def terminate_reservation(self, worker_id):
        ret = await self.client.call.terminate_reservation(worker_id)
        return  ret

    async def get_status(self):
        ret = await self.client.call.get_status()
        return  ret

    async def terminate_server(self):
        ret = await self.client.call.terminate_server()
        return  ret