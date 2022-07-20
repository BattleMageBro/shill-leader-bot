from aiogram import types
from core import dp, bot
import datetime
from messages import ERRORS
from states import BotStates
import asyncio
from logg import log
from exceptions import UserError, ChatError, to_custom_exc
from postgres.handlers import user_handler, chat_handler


current_transitions = []

@dp.message_handler(state='*', commands=['start_shilling'], chat_type=types.ChatType.PRIVATE)
async def shill_start(message: types.Message):
    # ToDo создать спейс транзишенов в постгре и записывать туда все а не в оперативку
    user_uuid = message.from_user.id
    try:
        if user_uuid in current_transitions:
            raise UserError(
                user_message=ERRORS['already_shilling'],
                dev_message='Double shilling by user {}'.format(user_uuid)
            )
        current_transitions.append(user_uuid)
        _, chat_uuid = await user_handler.get_user_with_chat(user_uuid)
        chat = await chat_handler.get(chat_uuid)
        end_timeout = chat.get('shill_end', 1) * 3600
        end_time = datetime.datetime.now().timestamp() + end_timeout
        shill_messages = ['3', '2', '1'].append(chat['shill_message'])
        msg_timeout, shill_timeout = chat['msg_timeout'], chat['shill_timeout']
        if not chat['shill_links'] or not chat['shill_message']:
            raise ChatError(
                user_message=ERRORS['start_shilling'],
                dev_message='Start shilling without options user {}'.format(user_uuid)
            )
        while datetime.datetime.now().timestamp() < end_time and user_uuid in current_transitions:
            for link in chat['shill_links']:
                shill_messages = ['3', '2', '1']
                shill_messages.append(chat["shill_message"])
                shill_messages.append(link)
                for item in shill_messages:
                    await bot.send_message(chat_id=chat_uuid, text=item)
                    await asyncio.sleep(msg_timeout)
                await asyncio.sleep(shill_timeout)
                if user_uuid not in current_transitions or datetime.datetime.now().timestamp() > end_time:
                    break
        if user_uuid in current_transitions:
            current_transitions.remove(user_uuid)
    except Exception as exc:
        exc = to_custom_exc(exc, user_uuid)
        log.error(exc.dev_message)
        await message.answer(exc.user_message)
        current_transitions.remove(user_uuid)
        return

@dp.message_handler(state='*', commands=['stop_shilling'], chat_type=types.ChatType.PRIVATE)
async def shill_stop(message:types.Message):
    # ToDo создать спейс транзишенов в постгре и записывать туда все а не в оперативку
    if message.from_user.id in current_transitions:
        current_transitions.remove(message.from_user.id)
