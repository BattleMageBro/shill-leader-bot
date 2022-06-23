import asyncio
import asyncpg

from logg import logger

class Postgres():
    def __init__(self, conn_string, pool_size):
        self.conn_string = conn_string
        self.pool = None
        self.pool_size = pool_size

    async def create_pool(self):
        while not self.pool:
            try:
                logger.debug(self.conn_string)
                self.pool = await asyncpg.create_pool(dsn=self.conn_string, command_timeout=60, max_size=self.pool_size)
                logger.info('postgres.create_pool succesfully')
            except Exception as exc:
                logger.error(f'postgres.create_pool catch exception when connect: {exc}')
                await asyncio.sleep(10)
        return f'successfully created pool: {self.pool}'

    async def select(self, table, index, value):
        if not self.pool:
            raise
        async with self.pool.acquire() as conn:
            if type(value) == str:
                value = f"'{value}'"
            if type(value) == int:
                value = f"{value}"
            text = f"SELECT * FROM {table} WHERE {index}={value}"
            logger.debug(text)
            res = await conn.fetch(text)
            logger.debug(res)
            if not res:
                raise Exception('no data in database')
            return res

    async def insert(self, table, data):
        if not self.pool:
            raise
        async with self.pool.acquire() as conn:
            indexes = ', '.join(data)
            values = ""
            for item in data.values():
                if type(item) == str:
                    item_str = f"'{item}'"
                    if not values:
                        values = f"{item_str}"
                    else:
                        values = f"{values}, {item_str}"
                if type(item) == int:
                    item_int = f"{item}"
                    if not values:
                        values = f"{item_int}"
                    else:
                        values = f"{values}, {item_int}"
            text = f"INSERT INTO {table} ({indexes}) VALUES ({values});"
            logger.debug(text)
            res = await conn.fetch(text)
            logger.debug(res)
            return res

    async def update(self, table, index, select_index, data):
        if not self.pool:
            raise
        async with self.pool.acquire() as conn:
            values = ""
            for key in data:
                value = data[key]
                if type(value) == str:
                    item = f"'{value}'"
                elif type(value) == int:
                    item = f"{value}"
                else:
                    item = f"{value}"
                if not values:
                    values = f"{key} = {item}"
                else:
                    values = f"{values}, {key} = {item}"
            select_cond = f"{index} = {select_index}"
            text = f"UPDATE {table} SET {values} WHERE {select_cond};"
            logger.debug(text)
            res = await conn.fetch(text)
            logger.debug(res)
            return res
        


