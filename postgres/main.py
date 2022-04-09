import asyncio
import asyncpg

class Postgres():
    def __init__(self, conn_string, db_table):
        self.conn_string = conn_string
        self.conn = None
        self.db_table = db_table

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

    async def get(self, id):
        text = f"SELECT * FROM {self.db_table} WHERE chat_id={id}"
        print(text)
        res = await self.conn.fetch(text)
        print(res)
        if not res:
            raise Exception('no data in database')
        return res

    async def insert(self, data):
        indexes = ', '.join(data)
        values = ""
        for item in data.values():
            if type(item) == str:
                item_str = f"'{item}'"
                if not values:
                    values = f"{item_str},"
                else:
                    values = f"{values} {item_str},"
            if type(item) == int:
                item_int = f"{item}"
                if not values:
                    values = f"{item_int},"
                else:
                    values = f"{values} {item_int},"
        values = values[:-1]
        text = f"INSERT INTO {self.db_table} ({indexes}) VALUES ({values});"
        print(text)
        res = await self.conn.fetch(text)
        print(res)
        return res

        


