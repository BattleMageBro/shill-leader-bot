import asyncio
import json
from functools import wraps
from aiogram import types
from core import dp, bot
from messages import MESSAGES
from states import BotStates
from postgres.handlers import user_handler, chat_handler
from exceptions import to_custom_exc
from logg import log


info_shema = {
    'ChatName': 'chat_name',
    'ShillMessage': 'shill_message',
    'Links': 'shill_links',
    'Timeout': 'shill_timeout',
    'EndTime': 'shill_end'
}



@dp.message_handler(state='*', commands=['setstate'], chat_type=types.ChatType.PRIVATE)
async def process_setstate_command(message: types.Message):
    argument = message.get_args()
    state = dp.current_state(user=message.from_user.id)
    if not argument:
        await state.reset_state()
        return await message.reply(MESSAGES['stateReset'])

    if (not argument.isdigit()) or (not int(argument) < len(BotStates.all())):
        return await message.reply(MESSAGES['invalidKey'].format(key=argument))

    await state.set_state(BotStates.all()[int(argument)])
    await message.reply(MESSAGES['stateChange'], reply=False)

@dp.message_handler(state='*', commands=['getstate'], chat_type=types.ChatType.PRIVATE)
async def process_setstate_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)

    await message.reply(f'Current state is {await state.get_state()}')

@dp.message_handler(state=[None, BotStates.PENDING[0]], commands=['help'], chat_type=types.ChatType.PRIVATE)
async def help_case(message: types.Message):
    await message.answer(MESSAGES['help'])

async def to_chat_info_message(chat):
    chat = dict(chat)
    res = ''
    for item in info_shema:
        res = f'{res}{item} - {chat[info_shema[item]]}\n' 
    return res

@dp.message_handler(state='*', commands=['get_chat_info'], chat_type=types.ChatType.PRIVATE)
async def get_chat_options(message:types.Message):
    user_uuid = message.from_user.id
    _, chat_uuid = await user_handler.get_user_with_chat(user_uuid)
    chat = await chat_handler.get(chat_uuid)
    await message.answer(await to_chat_info_message(chat))


@dp.message_handler(state=BotStates.all(), chat_type=types.ChatType.PRIVATE)
async def some_test_state_case_met(message: types.Message):
    text = 'wtf noone catch this before'
    await message.reply(text, reply=False)
