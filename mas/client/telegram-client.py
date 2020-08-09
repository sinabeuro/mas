import logging
import pprint
from aiogram import Bot, Dispatcher, executor, types
from mas.lib import Client

API_TOKEN = 'enter your token'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
cli = None
users = []

async def notify(result):
    for user in users:
        await bot.send_message(user, result)

@dp.message_handler(commands=['s', 'start'])
async def send_welcome(message: types.Message):
    global cli
    global users
    users.append(message.chat.id)

    cli = Client()
    await cli.connect(notify=notify)
    """
    This handler will be called when client send `/start` or `/help` commands.
    """
    if cli is not None:
        await message.reply("Connection succeeded")
    else:
        await message.reply("Connection failed")

@dp.message_handler(commands=['r', 'request'])
async def request_reservation(message: types.Message):
    args = message.text.split()[1:]

    ret = await cli.request_reservation(*args)
    if ret >= 0:
        await bot.send_message(message.chat.id, "Request succeeded, Worker : %d" % ret)
    else:
        await bot.send_message(message.chat.id, "Request failed")

@dp.message_handler(commands=['t', 'terminate'])
async def terminate_reservation(message: types.Message):
    args = message.text.split()[1:]

    ret = await cli.terminate_reservation(int(*args))
    if ret == 0:
        await bot.send_message(message.chat.id, "Termination succeeded")
    else:
        await bot.send_message(message.chat.id, "Termination failed")

@dp.message_handler(commands=['stat', 'status'])
async def get_status(message: types.Message):

    ret = await cli.get_status()
    if ret is not {}:
        await bot.send_message(message.chat.id, pprint.pformat(ret, indent=4))
    else:
        await bot.send_message(message.chat.id, "Get status failed")

@dp.message_handler()
async def echo(message: types.Message):
    await bot.send_message(message.chat.id, "Invalid command")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)