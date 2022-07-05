from aiogram import types
from asyncpg import UniqueViolationError
from core import dp, bot, postgres
from handler.utils import is_group
from postgres.handlers import user_handler, chat_handler, user_chat_handler
from logg import log
from messages import MESSAGES
from exceptions import to_custom_exc
from states import BotStates


async def check_create_chat(chat_uuid):
    chat = await chat_handler.get(chat_uuid)
    log.debug(chat)
    if not chat:
        data = {'chat_uuid': chat_uuid}
        await chat_handler.post(data)
    return chat

@dp.message_handler(state='*', commands=['choose_chat'])
async def choose_chat_start(message:types.Message):
    user_uuid = message.from_user.id
    chats = await user_chat_handler.get_chats_by_user(user_uuid)
    state = dp.current_state(user=user_uuid)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for item in chats:
        keyboard.add(str(item['chat_uuid']))
    await state.set_state(BotStates.CHOOSE_CHAT[0])
    await message.answer(MESSAGES['choose_chat'], reply_markup=keyboard)

@dp.message_handler(state=[BotStates.CHOOSE_CHAT[0]])
async def choose_chat(message:types.Message):
    user_uuid = message.from_user.id
    state = dp.current_state(user=user_uuid)
    try:
        await user_handler.patch(user_uuid, {'current_chat': message.text})
    except Exception as exc:
        exc = to_custom_exc(exc, message.from_user.id)
        log.error(exc.dev_message)
        await message.answer(exc.user_message)
        return
    finally:
        await state.set_state(BotStates.PENDING[0])
    await message.answer(MESSAGES['choose_chat'])
    

@dp.message_handler(state='*', commands=['add_shillbot'])
async def create_user_chat(message: types.Message):
    if not is_group(message.chat.type):
        return
    member = await message.chat.get_member(message.from_user.id)
    if not member.is_chat_admin():
        return
    try:
        user_uuid = message.from_user.id
        chat_uuid = message.chat.id
        await check_create_chat(chat_uuid)
        if not await user_chat_handler.have_link(user_uuid, chat_uuid):
            await user_chat_handler.post({"user_uuid": user_uuid, "chat_uuid": chat_uuid})
            await user_handler.patch(user_uuid, {'current_chat': chat_uuid})
            log.info("User with id {} successfully added chat with id {} to chats".format(user_uuid, chat_uuid))

        await message.reply(MESSAGES['chat_added'])
    except Exception as exc:
        exc = to_custom_exc(exc, message.from_user.id)
        log.error(exc.dev_message)
        await message.answer(exc.user_message)
        return


# --------------- for tests ---------------

@dp.message_handler(state=[None], commands='test2')
async def test_handler(message: types.Message):
    user = await user_handler.get(message.from_user.id)
    log.debug(user['user_uuid'])
    log.debug(user['current_chat'])