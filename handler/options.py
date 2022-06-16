from aiogram import types
from core import dp, bot, postgres
from states import BotStates
from handler.utils import is_private
from messages import MESSAGES

@dp.message_handler(state=[BotStates.CHOOSE_CHAT[0]])
async def choose_chat(message:types.Message):
    await message.answer(MESSAGES['choose_chat'])
    await message.answer(MESSAGES['choose_options'])


@dp.message_handler(state=[None, BotStates.PENDING[0]], commands=['choose_options'])
async def start_choosing_options(message:types.Message):
    user_id = message.from_user.id
    user = await postgres.select('users', 'user_uuid', message.from_user.id)[0]
    chat = await postgres.select('chat', 'chat_uuid', user['current_chat'])[0]
    #next step is choose shill message 
    #then links
    #then timeout   
    # ToDo : add packs

    state = dp.current_state(user=message.from_user.id)
    await state.set_state(CHOOSE_CHAT[0])
    await message.answer(MESSAGES['choose_options'])



