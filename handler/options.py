import json

from aiogram import types
from core import dp
from states import BotStates
from messages import MESSAGES
from logg import log
from exceptions import to_custom_exc
from postgres.handlers import user_handler, chat_handler


async def shill_message(message:types.Message):
    user_uuid = message.from_user.id
    user, chat_uuid = await user_handler.get_user_with_chat(user_uuid)

    shill_message = message.text
    data = {'shill_message': shill_message}
    await chat_handler.patch(chat_uuid, data)
    await message.answer(MESSAGES['choose_shill_message_success'])

@dp.message_handler(state='*', commands=['get_chat_info'])
async def get_chat_options(message:types.Message):
    user_uuid = message.from_user.id
    try:
        user, chat_uuid = await user_handler.get_user_with_chat(user_uuid)
        chat = await chat_handler.get(chat_uuid)
        result = json.dumps(chat)
        await message.answer(result)
    except Exception as exc:
        exc = to_custom_exc(exc, user_uuid)
        log.error(exc.dev_message)
        await message.answer(exc.user_message)
        return

@dp.message_handler(state=[None, BotStates.PENDING[0]], commands=['choose_options'])
async def start_choosing_options(message:types.Message):
    user_uuid = message.from_user.id
    state = dp.current_state(user=user_uuid)
    try:
        await user_handler.get_user_with_chat(user_uuid)
        await state.set_state(BotStates.CHOOSE_SHILL_MESSAGE_OPTS[0])
        await message.answer(MESSAGES['choose_options'])
        await message.answer(MESSAGES['choose_shill_message'])
    except Exception as exc:
        exc = to_custom_exc(exc, user_uuid)
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
    user_uuid = message.from_user.id
    state = dp.current_state(user=user_uuid)
    try:
        user, chat_uuid = await user_handler.get_user_with_chat(user_uuid)

        links = message.text.strip(' ').split(',')
        data = {'links': links}
        await chat_handler.patch(chat_uuid, data)
        await message.answer(MESSAGES['choose_links_success'])

        
        await state.set_state(BotStates.CHOOSE_TIMEOUT[0])
        await message.answer(MESSAGES['choose_timeout'])
    except Exception as exc:
        exc = to_custom_exc(exc, user_uuid)
        log.error(exc.dev_message)
        await state.set_state(BotStates.PENDING[0])
        await message.answer(exc.user_message)
        return
