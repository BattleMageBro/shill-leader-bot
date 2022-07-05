from aiogram import types
from core import dp, bot
import os, time
import datetime
from messages import MESSAGES
from states import BotStates
import asyncio
from handler import utils
from logg import log
from exceptions import UserError, to_custom_exc
from postgres.handlers import user_handler, chat_handler


current_transitions = []

@dp.message_handler(state='*', commands=['shill_start'])
async def shill_start(message: types.Message):
    if not utils.is_private(message.chat.type):
        return
    # ToDo создать спейс транзишенов в постгре и записывать туда все а не в оперативку
    user_uuid = message.from_user.id
    try:
        if user_uuid in current_transitions:
            raise UserError(
                user_message='You already shilling. End shill with /end_shill command, choose other chat and options if needed and start again',
                dev_message='Double shilling by user {}'.format(user_uuid)
            )
        current_transitions.append(user_uuid)
        user, chat_uuid = await user_handler.get_user_with_chat(user_uuid)
        chat = await chat_handler.get(chat_uuid)
        end_time = datetime.datetime.now().timestamp() + 59 # ToDo create config parameter
        shill_messages = ['3', '2', '1'].append(chat['shill_message'])
        msg_timeout, shill_timeout = chat['msg_timeout'], chat['shill_timeout']
        while datetime.datetime.now().timestamp() < end_time and user_uuid in current_transitions:
            for link in chat['shill_links']:
                msg = f'{link}  -  {chat["shill_message"]}'
                shill_messages = ['3', '2', '1']
                shill_messages.append(msg)
                for item in shill_messages:
                    await bot.send_message(chat_id=chat_uuid, text=item)
                    await asyncio.sleep(msg_timeout)
                await asyncio.sleep(shill_timeout)
                if user_uuid not in current_transitions:
                    break
        if user_uuid in current_transitions:
            current_transitions.remove(user_uuid)
    except Exception as exc:
        exc = to_custom_exc(exc, user_uuid)
        log.error(exc.dev_message)
        await message.answer(exc.user_message)
        current_transitions.remove(user_uuid)
        return

@dp.message_handler(state='*', commands=['shill_stop'])
async def shill_stop(message:types.Message):
    if not utils.is_private(message.chat.type):
        return
    # ToDo создать спейс транзишенов в постгре и записывать туда все а не в оперативку
    if message.from_user.id in current_transitions:
        current_transitions.remove(message.from_user.id)

@dp.message_handler(state=[None, BotStates.PENDING])
async def first_test_state_case_met(message: types.Message):
    if not utils.is_private(message.chat.type):
        return
    log.debug(message)
    await message.reply('мы на самом старте!', reply=False)

@dp.message_handler(state=BotStates.all())
async def some_test_state_case_met(message: types.Message):
    if not utils.is_private(message.chat.type):
        return
    text = 'wtf noone catch this before'
    await message.reply(text, reply=False)
