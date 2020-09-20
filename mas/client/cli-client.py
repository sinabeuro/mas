import argparse
import asyncio
import logging
import pprint

from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory

from mas.lib import Client


def notify(result):
    if result == -1:
        print(f'The server has been shut down.')
        tasks = [
            t for t in asyncio.all_tasks() if t is not asyncio.current_task()
        ]
        [task.cancel() for task in tasks]
        return
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

    ret = None
    try:
        ret = await cli.connect(notify=notify)
    except asyncio.TimeoutError:
        print('Could not connect.')
        return

    ret = await rpc(cli, args)
    if ret is None:
        session = PromptSession(
            'cli-client> ',
            history=FileHistory('.cli-client-history'),
            auto_suggest=AutoSuggestFromHistory(),
        )

        on_prompt = True
        while on_prompt:
            try:
                args = await session.prompt_async()
                if args == 'exit':
                    raise EOFError
                args = parser.parse_known_args(args.split())
                ret = await rpc(cli, args[0])
                pprint.pprint(ret)
            except SystemExit:
                pass
            except (asyncio.TimeoutError, asyncio.CancelledError):
                print('Connection is not valid.')
                return
            except KeyboardInterrupt:
                print('KeyboardInterrupt')
            except EOFError:
                on_prompt = False
    else:
        pprint.pprint(ret)

    try:
        await cli.disconnect()
    except asyncio.TimeoutError:
        print('Connection is not valid.')


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
