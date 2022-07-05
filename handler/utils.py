import asyncio
from functools import wraps
from aiogram import types
from core import dp, bot
from messages import MESSAGES
from states import BotStates


def is_private(mes_type):
    if mes_type == 'private':
        return True
    return False

def is_group(mes_type):
    if mes_type == 'group':
        return True
    return False

@dp.message_handler(state='*', commands=['setstate'])
async def process_setstate_command(message: types.Message):
    if not is_private(message.chat.type):
        return
    argument = message.get_args()
    state = dp.current_state(user=message.from_user.id)
    if not argument:
        await state.reset_state()
        return await message.reply(MESSAGES['stateReset'])

    if (not argument.isdigit()) or (not int(argument) < len(BotStates.all())):
        return await message.reply(MESSAGES['invalidKey'].format(key=argument))

    await state.set_state(BotStates.all()[int(argument)])
    await message.reply(MESSAGES['stateChange'], reply=False)

@dp.message_handler(state='*', commands=['getstate'])
async def process_setstate_command(message: types.Message):
    if not is_private(message.chat.type):
        return
    state = dp.current_state(user=message.from_user.id)

    await message.reply(f'Current state is {await state.get_state()}')

@dp.message_handler(state=[None, BotStates.PENDING[0]], commands=['help'])
async def help_case(message: types.Message):
    if not is_private(message.chat.type):
        return
    await message.answer(MESSAGES['help'])


# does not work =(
# def is_private(func):
#     @wraps(func)
#     async def wrap(message):
#         print('123')
#         if message.chat.type == 'private':
#             return
#         return await func(message)
#     return wrap
