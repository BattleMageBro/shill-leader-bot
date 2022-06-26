from aiogram import types
from core import dp, bot, postgres
from states import BotStates
from handler.utils import is_private
from messages import MESSAGES
from logg import log
from exceptions import UserError, to_custom_exc
from postgres.handlers import user_handler, chat_handler


@dp.message_handler(state=[BotStates.CHOOSE_CHAT[0]])
async def choose_chat(message:types.Message):
    await message.answer(MESSAGES['choose_chat'])
    await message.answer(MESSAGES['choose_options'])

async def shill_message(message:types.Message):
    user_id = message.from_user.id
    user, chat_uuid = await user_handler.get_user_with_chat(user_id)

    shill_message = message.text
    data = {'shill_message': shill_message}
    await chat_handler.patch(chat_uuid, data)
    await message.answer(MESSAGES['choose_shill_message_success'])

@dp.message_handler(state=[None, BotStates.PENDING[0]], commands=['choose_options'])
async def start_choosing_options(message:types.Message):
    user_id = message.from_user.id
    state = dp.current_state(user=user_id)
    try:
        await state.set_state(BotStates.CHOOSE_SHILL_MESSAGE_OPTS[0])
        await message.answer(MESSAGES['choose_options'])
        await message.answer(MESSAGES['choose_shill_message'])
    except Exception as exc:
        exc = to_custom_exc(exc, user_id)
        log.error(exc.dev_message)
        await state.set_state(BotStates.PENDING[0])
        await message.answer(exc.user_message)
        return
    #next step is choose shill message 
    #then links
    #then timeout   
    # ToDo : add packs

@dp.message_handler(state=[BotStates.CHOOSE_SHILL_MESSAGE_OPTS[0]])
async def choose_shill_message_opts(message:types.Message):
    state = dp.current_state(user=message.from_user.id)
    try:
        await shill_message(message)

        await state.set_state(BotStates.CHOOSE_LINKS_OPTS[0])
        await message.answer(MESSAGES['choose_links'])
    except Exception as exc:
        exc = to_custom_exc(exc, message.from_user.id)
        log.error(exc.dev_message)
        await state.set_state(BotStates.PENDING[0])
        await message.answer(exc.user_message)
        return

@dp.message_handler(state=[BotStates.CHOOSE_SHILL_MESSAGE[0]])
async def choose_shill_message(message:types.Message):
    state = dp.current_state(user=message.from_user.id)
    try:
        await shill_message(message)

        await state.set_state(BotStates.PENDING[0])
    except Exception as exc:
        exc = to_custom_exc(exc, message.from_user.id)
        log.error(exc.dev_message)
        await state.set_state(BotStates.PENDING[0])
        await message.answer(exc.user_message)
        return

@dp.message_handler(state=[BotStates.CHOOSE_LINKS_OPTS[0]])
async def choose_links_opts(message:types.Message):
    user_id = message.from_user.id
    state = dp.current_state(user=user_id)
    try:
        user, chat_uuid = await user_handler.get_user_with_chat(user_id)

        links = message.text.strip(' ').split(',')
        data = {'links': links}
        await chat_handler.patch(chat_uuid, data)
        await message.answer(MESSAGES['choose_links_success'])

        
        await state.set_state(BotStates.CHOOSE_TIMEOUT[0])
        await message.answer(MESSAGES['choose_timeout'])
    except Exception as exc:
        exc = to_custom_exc(exc, user_id)
        log.error(exc.dev_message)
        await state.set_state(BotStates.PENDING[0])
        await message.answer(exc.user_message)
        return
