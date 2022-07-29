import aiogram
from core import dp, shutdown, loop
from aiogram import executor
import importlib
import asyncio
from exceptions import to_custom_exc

from logg import log

importlib.import_module('handler.errors')
importlib.import_module('handler.user')
importlib.import_module('handler.chat')
importlib.import_module('handler.options')
importlib.import_module('handler.shiller')
importlib.import_module('handler.utils')


if __name__ == '__main__':
    log.info('Start executing application')
    executor.start_polling(dp, on_shutdown=shutdown, loop=loop)
