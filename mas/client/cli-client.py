import asyncio
from mas.lib import Client
import argparse
import pprint
import logging
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

def notify(result):
    print(result)

async def rpc(cli, args):
    try:
        if args.__contains__('request_args'):
            ret = await cli.request(*args.request_args)
        elif args.__contains__('terminate_args'):
            ret = await cli.terminate(int(*args.terminate_args))
        elif args.__contains__('status'):
            ret = await cli.status()
        else:
            ret = None
        return ret
    except TypeError as e:
        logger.error(e)

async def main(args):
    cli = Client()
    ret = await cli.connect(notify=notify)
    ret = await rpc(cli, args)
    if ret is None:
        session = PromptSession('cli-client> ',
            history=FileHistory('.cli-client-history'),
            auto_suggest=AutoSuggestFromHistory())

        while True:
            try:
                args = await session.prompt_async()
                if args == 'exit':
                    break
                args = parser.parse_known_args(args.split())
                ret = await rpc(cli, args[0])
                pprint.pprint(ret)
            except SystemExit:
                pass
            except KeyboardInterrupt:
                print("KeyboardInterrupt")
            except EOFError:
                return
    else:
        pprint.pprint(ret)

logger = logging.getLogger()
parser = argparse.ArgumentParser(prog='cli-client')
sub_parsers = parser.add_subparsers()
r_parser = sub_parsers.add_parser('request')
r_parser.add_argument('request_args', nargs='+')
t_parser = sub_parsers.add_parser('terminate')
t_parser.set_defaults(terminate=True)
t_parser.add_argument('terminate_args', nargs='+')
s_parser = sub_parsers.add_parser('status')
s_parser.set_defaults(status=True)

args = parser.parse_args()
loop = asyncio.get_event_loop()
loop.run_until_complete(main(args))
