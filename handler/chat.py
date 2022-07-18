from aiogram import types
from asyncpg import UniqueViolationError
from core import dp, bot, postgres
from postgres.handlers import user_handler, chat_handler, user_chat_handler
from logg import log
from messages import MESSAGES, ERRORS
from exceptions import to_custom_exc, ChatError
from states import BotStates
from aiogram.dispatcher.filters import Text


async def check_create_chat(chat_uuid:int, chat_name:str):
    chat = await chat_handler.get(chat_uuid)
    log.debug(chat)
    if not chat:
        data = {'chat_uuid': chat_uuid, 'chat_name': chat_name}
        await chat_handler.post(data)
    return chat

@dp.message_handler(state='*', commands=['choose_chat'], chat_type=types.ChatType.PRIVATE)
async def choose_chat_start(message:types.Message):
    user_uuid = message.from_user.id
    chats = await user_chat_handler.get_chats_with_names(user_uuid)
    if not chats:
        await message.answer(ERRORS['no_chats'])
        return
    state = dp.current_state(user=user_uuid)
    inline_keyboard = types.InlineKeyboardMarkup(row_width=2)
    for item in chats:
        inline_keyboard.add(types.InlineKeyboardButton(text=str(item['chat_name']), callback_data=str(item['chat_uuid'])))
    await state.set_state(BotStates.CHOOSE_CHAT[0])
    await message.answer(MESSAGES['choose_chat'], reply_markup=inline_keyboard)

@dp.callback_query_handler(lambda callback: callback.data.startswith('-'), state='*')
async def choose_chat(callback_query:types.CallbackQuery):
    log.debug(callback_query)
    user_uuid = callback_query.from_user.id
    chat_uuid = callback_query.data
    state = dp.current_state(user=user_uuid)
    try:
        chat = await chat_handler.get(chat_uuid)
        if not chat:
            raise ChatError(
                user_message=ERRORS['chat_not_exist'],
                dev_message="User with id {} try to choose chat with id {} as current. Chat not found".format(user_uuid, chat_uuid)
            )
        await user_handler.patch(user_uuid, {'current_chat': chat_uuid})
    except Exception as exc:
        exc = to_custom_exc(exc, user_uuid)
        log.error(exc.dev_message)
        await callback_query.message.answer(exc.user_message)
        return
    finally:
        await state.set_state(BotStates.PENDING[0])
    await callback_query.message.answer(MESSAGES['choose_chat_success'])
    await callback_query.answer()

@dp.message_handler(state='*', commands=['add_shillbot'], is_chat_admin=True)
async def create_user_chat(message: types.Message):
    try:
        user_uuid = message.from_user.id
        chat_uuid = message.chat.id
        await check_create_chat(chat_uuid, message.chat.title)
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
