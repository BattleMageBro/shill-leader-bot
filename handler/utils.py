import asyncio
from functools import wraps


def is_private(mes_type):
    if mes_type == 'private':
        return True
    return False

def is_group(mes_type):
    if mes_type == 'group':
        return True
    return False

# does not work =(
# def is_private(func):
#     @wraps(func)
#     async def wrap(message):
#         print('123')
#         if message.chat.type == 'private':
#             return
#         return await func(message)
#     return wrap
