import json

from aiogram import types
from core import dp
from states import BotStates
from messages import MESSAGES
from logg import log
from exceptions import to_custom_exc
from postgres.handlers import user_handler, chat_handler


@dp.message_handler(state=[None, BotStates.PENDING[0]], commands=['choose_options'], chat_type=types.ChatType.PRIVATE)
async def start_choosing_options(message:types.Message):
    #toDo перепилить блок чтобы тут было на выбор выподали ключи как в чатах, паки или самостоятельно . И в состояние ЧУЗ_ПАК_ОР_СЕЛФ
    #toDO далее по проуессам идем в выбор шил сообщения потом тамер, добавить таймер в бд на выключения шилпроцесса
    #toDo надо зафигачить нейм в чатах и иннер джойн на присоединение их из другой таблички
    #toDo еще надо добавить комманды для помощи хелп коммандс и тд
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
    # ToDo : add packs



async def shill_message(message:types.Message):
    user_uuid = message.from_user.id
    _, chat_uuid = await user_handler.get_user_with_chat(user_uuid)

    shill_message = message.text
    data = {'shill_message': shill_message}
    await chat_handler.patch(chat_uuid, data)
    await message.answer(MESSAGES['choose_shill_message_success'].format(shill_message))

@dp.message_handler(state=[BotStates.CHOOSE_SHILL_MESSAGE_OPTS[0]], chat_type=types.ChatType.PRIVATE)
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

@dp.message_handler(state=[BotStates.CHOOSE_SHILL_MESSAGE[0]], chat_type=types.ChatType.PRIVATE)
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

@dp.message_handler(state=[BotStates.CHOOSE_LINKS_OPTS[0]], chat_type=types.ChatType.PRIVATE)
async def choose_links_opts(message:types.Message):
    user_uuid = message.from_user.id
    state = dp.current_state(user=user_uuid)
    try:
        _, chat_uuid = await user_handler.get_user_with_chat(user_uuid)

        links = message.text.replace(' ', '').split(',')
        data = {'shill_links': links}
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

@dp.message_handler(state=[BotStates.CHOOSE_TIMEOUT[0]], chat_type=types.ChatType.PRIVATE)
async def choose_timeout(message:types.Message):
    user_uuid = message.from_user.id
    state = dp.current_state(user=user_uuid)
    try:
        _, chat_uuid = await user_handler.get_user_with_chat(user_uuid)
        data = {'shill_timeout': int(message.text)}
        await chat_handler.patch(chat_uuid, data)
        await state.set_state(BotStates.PENDING[0])
        await message.answer(MESSAGES['choose_timeout_success'].format(int(message.text)))
    except Exception as exc:
        exc = to_custom_exc(exc, user_uuid)
        log.error(exc.dev_message)
        await state.set_state(BotStates.PENDING[0])
        await message.answer(exc.user_message)
        return

@dp.message_handler(state='*', commands=['get_chat_info'], chat_type=types.ChatType.PRIVATE)
async def get_chat_options(message:types.Message):
    user_uuid = message.from_user.id
    try:
        _, chat_uuid = await user_handler.get_user_with_chat(user_uuid)
        chat = await chat_handler.get(chat_uuid)
        await message.answer(chat)
    except Exception as exc:
        exc = to_custom_exc(exc, user_uuid)
        log.error(exc.dev_message)
        await message.answer(exc.user_message)
        return
