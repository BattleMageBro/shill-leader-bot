from core import dp, shutdown, loop
from aiogram import executor
import importlib

importlib.import_module('handler.chat')
importlib.import_module('handler.options')
importlib.import_module('handler.shiller')


if __name__ == '__main__':
    print("start")
    executor.start_polling(dp, on_shutdown=shutdown, loop=loop)