from core import dp, shutdown
from aiogram import executor
import importlib

importlib.import_module('handler.shiller')


if __name__ == '__main__':
    print("start")
    executor.start_polling(dp, on_shutdown=shutdown)