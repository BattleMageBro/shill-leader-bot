from aiogram import types
from core import dp, bot, postgres
from states import BotStates
from handler.utils import is_private
from messages import MESSAGES

async def choose_chat(message:types.Message):
    await message.answer(MESSAGES['choose_chat'])
    await message.answer(MESSAGES['choose_options'])

@dp.message_handler(state=[None, BotStates.PENDING[0]], commands=['choose_options'])
async def start_choosing_options(message:types.Message):
    resp = await postgres.get('user_uuid', message.from_user.id)
    chat_count = len(resp)
    if chat_count != 1:
        res = await choose_chat(message)
        return
    await message.answer(MESSAGES['choose_options'])
