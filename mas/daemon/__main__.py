import asyncio
from mas import Mas
from mas.daemon import Worker

async def main():
    mas = Mas()
    await mas.start()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())