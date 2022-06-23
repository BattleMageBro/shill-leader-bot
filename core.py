import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from postgres.main import Postgres
from config import config
from logg import logger

loop = asyncio.get_event_loop()

TOKEN = config['TOKEN']
bot = Bot(token=TOKEN, loop=loop)
dp =  Dispatcher(bot, storage=MemoryStorage())

SQL_CONN_STRING = f"postgresql://{config['SQL_HOST']}:{config['SQL_PORT']}/{config['SQL_DB']}?user={config['SQL_USER']}&password={config['SQL_PASSWORD']}"
POOL_SIZE = 10
postgres = Postgres(SQL_CONN_STRING, POOL_SIZE)

async def postgres_task():
    conn = await postgres.create_pool()
    logger.info(f'qwe {conn}')

loop.run_until_complete(postgres_task())

async def shutdown(dispatcher: Dispatcher):
    """
    :param dispatcher:
    :return:
    """
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()