from core import dp, shutdown, loop
from aiogram import executor
import importlib

from logg import log

importlib.import_module('handler.user')
importlib.import_module('handler.chat')
importlib.import_module('handler.options')
importlib.import_module('handler.shiller')


if __name__ == '__main__':

    log.info('Start executing application')
    executor.start_polling(dp, on_shutdown=shutdown, loop=loop)