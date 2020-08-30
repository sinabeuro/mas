import asyncio
from mas.lib import Client
import argparse
import pprint

def notify(result):
    print(result)

async def main(args):
    cli = Client()
    await cli.connect(notify=notify)

    if args.request is not None:
        ret = await cli.request(*args.request)
    elif args.terminate is not None:
        ret = await cli.terminate(int(*args.terminate))
    elif args.status is not None:
        ret = await cli.status()

    pprint.pprint(ret)

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--request', nargs='+')
parser.add_argument('-t', '--terminate', nargs='+')
parser.add_argument('--status', action='store_true')
args = parser.parse_args()

loop = asyncio.get_event_loop()
loop.run_until_complete(main(args))