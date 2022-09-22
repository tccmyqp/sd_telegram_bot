import os
import sys
import re

from loguru import logger


# level_per_module = {
#     "": "INFO",
#     "app.db.bot_db": "INFO",
#     "app.common": False
# }

# logger.add(lambda m: print(m, end=""), filter=level_per_module, level=0)

# logger.add(sys.stderr, level="ERROR", filter='DEBUG') 
# logger.add(sys.stdout, format="{time} - {level} - {message}", filter="app.common")

from importlib import import_module
from aiogram.types import BotCommand
from aiogram import Bot, Dispatcher
from app.config import token
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from app.strings import data_strings, data_polls
from app.db.bot_db import bot_db
from aiogram import types



# fmt = "{time}"
# fmt = "{time} - {name} - {level} - {message}"
# logger.add(level="DEBUG", format=fmt)
# logger.add(sys.stdout, level="INFO", format=fmt)

storage = MemoryStorage()

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
registered_users = bot_db.get_registered_users()


# установка описания к командам
async def set_start_commands(bot: Bot):
    client_commands = [
        BotCommand(command="/"+data_strings['cmd']['start']['cmd'], description=data_strings['cmd']['start']['descr']),
        BotCommand(command="/"+data_strings['cmd']['help']['cmd'], description=data_strings['cmd']['help']['descr']),
        BotCommand(command="/"+data_strings['cmd']['cancel']['cmd'], description=data_strings['cmd']['cancel']['descr']),
   ]
    await bot.set_my_commands(client_commands)

# установка описания к командам
async def set_client_commands(bot: Bot):
    client_commands = [
        BotCommand(command="/"+data_strings['cmd']['start']['cmd'], description=data_strings['cmd']['start']['descr']),
        BotCommand(command="/"+data_strings['cmd']['help']['cmd'], description=data_strings['cmd']['help']['descr']),
        BotCommand(command="/"+data_polls['map_poll']['cmd'], description=data_polls['map_poll']['descr']),
        BotCommand(command="/"+data_strings['cmd']['cancel']['cmd'], description=data_strings['cmd']['cancel']['descr']),
   ]
    await bot.set_my_commands(client_commands)

# установка описания к командам
async def set_admin_commands(bot: Bot):
    admin_commands = [
        BotCommand(command="/"+data_strings['cmd']['start']['cmd'], description=data_strings['cmd']['start']['descr']),
        BotCommand(command="/"+data_strings['cmd']['help']['cmd'], description=data_strings['cmd']['help']['descr']),
        BotCommand(command="/"+data_strings['cmd']['id']['cmd'], description=data_strings['cmd']['id']['descr']),
        BotCommand(command="/"+data_polls['map_poll']['cmd'], description=data_polls['map_poll']['descr']),
        BotCommand(command="/"+data_strings['cmd']['rst_map_poll']['cmd'], description=data_strings['cmd']['rst_map_poll']['descr']),
        BotCommand(command="/"+data_strings['cmd']['cancel']['cmd'], description=data_strings['cmd']['cancel']['descr']),
        
    ]
    await bot.set_my_commands(admin_commands)

def register_handlers_polls():
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(ROOT_DIR, 'polls')


    # print(os.getcwd())
    # path = 'app\polls'
    content = os.listdir(path)
    dirs = [i.name for i in os.scandir(path) if i.is_dir() and re.match(r'[^__]', i.name)]
    # print(dirs)

    # загружаем данные из polls
    poll_handlers = []
    for name in dirs:
            module = import_module(f'app.polls.{name}.poll_handlers')
            module.register_handlers(dp)