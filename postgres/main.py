import asyncio
import asyncpg

class Postgres():
    def __init__(self, conn_string):
        self.conn_string = conn_string
        self.conn = None

    async def connect(self):
        while not self.conn:
            try:
                print(self.conn_string)
                self.conn = await asyncpg.connect(self.conn_string)
                print('postgres.connect succesfully')
            except Exception:
                print(f'postgres.connect catch exception when connect: {Exception}')
                await asyncio.sleep(10)
        return '123'

    async def get(self, table, index, value):
        if type(value) == str:
            value = f"'{value}'"
        if type(value) == int:
            value = f"{value}"
        text = f"SELECT * FROM {table} WHERE {index}={value}"
        print(text)
        res = await self.conn.fetch(text)
        print(res)
        if not res:
            raise Exception('no data in database')
        return res

    async def insert(self, table, data):
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
        values = values[:-1]
        text = f"INSERT INTO {table} ({indexes}) VALUES ({values});"
        print(text)
        res = await self.conn.fetch(text)
        print(res)
        return res

    async def update(self, table, index, value, data):
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
        select_cond = f"{index} = {value}"
        text = f"UPDATE {table} SET {values} WHERE {select_cond};"
        print(text)
        res = await self.conn.fetch(text)
        print(res)
        return res
        


