import json

from aiogram import types
from core import dp
from states import BotStates
from messages import MESSAGES, ERRORS
from logg import log
from exceptions import to_custom_exc, ServiceError, OptsError
from postgres.handlers import user_handler, chat_handler, packs_handler


# this is options process step by step

@dp.message_handler(state=[None, BotStates.PENDING[0]], commands=['choose_options'], chat_type=types.ChatType.PRIVATE)
async def start_choosing_options(message:types.Message):
    user_uuid = message.from_user.id
    state = dp.current_state(user=user_uuid)
    await user_handler.get_user_with_chat(user_uuid)
    await state.set_state(BotStates.CHOOSE_PACK_OR_SELF[0])
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text='choose links from pack', callback_data='choose_packs'))
    keyboard.add(types.InlineKeyboardButton(text='choose links self', callback_data='choose_self'))
    await message.answer(MESSAGES['choose_options'], reply_markup=keyboard)

@dp.callback_query_handler(lambda callback: callback.data.startswith('choose'), state=BotStates.CHOOSE_PACK_OR_SELF[0])
async def choose_pack_or_self(callback:types.CallbackQuery):
    options = {
        'packs': {
            'func' : choose_packs,
            'state' : BotStates.CHOOSE_PACKS_OPTS[0],
            'msg' : MESSAGES['choose_packs_start']
        },
        'self': {
            'func' : None,
            'state' : BotStates.CHOOSE_LINKS_OPTS[0],
            'msg' : MESSAGES['choose_links']
        },
    }
    user_uuid = callback.from_user.id
    state = dp.current_state(user=user_uuid)
    try:
        choose_opt = callback.data.replace('choose_', '')
        opts = options.get(choose_opt, {})
        if not opts:
            raise OptsError(
                dev_message = "handler.options.choose_pach_or_self fail for user {} with data {}".format(user_uuid, callback.data),
                user_message = ERRORS['wrong_opts_data']
            )
        await callback.message.answer(opts['msg'])
        await state.set_state(opts['state'])
        if opts['func']:
            await opts['func'](callback.message)
    except Exception as exc:
        exc = to_custom_exc(exc, user_uuid)
        log.error(exc.dev_message)
        await callback.message.answer(exc.user_message)
        return
    await callback.answer()


async def choose_packs(message:types.Message):
    user_uuid = message.from_user.id
    try:
        state = dp.current_state(user=user_uuid)
        packs = await packs_handler.get_all()
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        for item in packs:
            keyboard.add(types.InlineKeyboardButton(text=item['pack_description'], callback_data=f'pack_{item["pack_uuid"]}'))
        await message.answer(MESSAGES['choose_packs'], reply_markup=keyboard)
        log.debug(packs)
    except Exception as exc:
        exc = to_custom_exc(exc, user_uuid)
        log.error(exc.dev_message)
        await message.answer(exc.user_message)
        return

@dp.callback_query_handler(lambda callback: callback.data.startswith('pack'), state=BotStates.CHOOSE_PACKS_OPTS[0])
async def choose_packs_opts_finish(callback:types.CallbackQuery):
    user_uuid = callback.from_user.id
    pack_uuid = callback.data.replace('pack_', '')
    state = dp.current_state(user=user_uuid)
    try:
        _, chat_uuid = await user_handler.get_user_with_chat(user_uuid)
        pack = await packs_handler.get(pack_uuid)
        data = {'shill_links': pack['shill_links']}
        await chat_handler.patch(chat_uuid, data)
        await state.set_state(BotStates.CHOOSE_SHILL_MESSAGE_OPTS[0])
        await callback.message.answer(MESSAGES['choose_packs_success'])
        await callback.message.answer(MESSAGES['choose_shill_message'])
    except Exception as exc:
        exc = to_custom_exc(exc, user_uuid)
        log.error(exc.dev_message)
        await callback.message.answer(exc.user_message)
        await state.set_state(BotStates.PENDING[0])
    finally:
        await callback.answer()

@dp.message_handler(state=[BotStates.CHOOSE_LINKS_OPTS[0]], chat_type=types.ChatType.PRIVATE)
async def choose_links_opts(message:types.Message):
    user_uuid = message.from_user.id
    state = dp.current_state(user=user_uuid)
    await links(message)
    await state.set_state(BotStates.CHOOSE_SHILL_MESSAGE_OPTS[0])
    await message.answer(MESSAGES['choose_shill_message'])

async def links(message:types.Message):
    _, chat_uuid = await user_handler.get_user_with_chat(message.from_user.id)

    links = message.text.replace(' ', '').split(',')
    data = {'shill_links': links}
    await chat_handler.patch(chat_uuid, data)
    await message.answer(MESSAGES['choose_links_success'])

@dp.message_handler(state=[BotStates.CHOOSE_SHILL_MESSAGE_OPTS[0]], chat_type=types.ChatType.PRIVATE)
async def choose_shill_message_opts(message:types.Message):
    state = dp.current_state(user=message.from_user.id)
    await shill_message(message)

    await state.set_state(BotStates.CHOOSE_TIMEOUT_OPTS[0])
    await message.answer(MESSAGES['choose_timeout'])


async def shill_message(message:types.Message):
    user_uuid = message.from_user.id
    _, chat_uuid = await user_handler.get_user_with_chat(user_uuid)

    shill_message = message.text
    data = {'shill_message': shill_message}
    await chat_handler.patch(chat_uuid, data)
    await message.answer(MESSAGES['choose_shill_message_success'].format(shill_message))

@dp.message_handler(state=[BotStates.CHOOSE_TIMEOUT_OPTS[0]], chat_type=types.ChatType.PRIVATE)
async def choose_timeout_opts(message:types.Message):
    user_uuid = message.from_user.id
    state = dp.current_state(user=user_uuid)
    try:
        _, chat_uuid = await user_handler.get_user_with_chat(user_uuid)
        timeout = float(message.text)
        data = {'shill_timeout': int(timeout)}
        await chat_handler.patch(chat_uuid, data)
        await message.answer(MESSAGES['choose_timeout_success'].format(int(timeout)))
        await message.answer(MESSAGES['choose_shill_end'])
        await state.set_state(BotStates.CHOOSE_SHILL_END[0])
    except ValueError:
        log.error("User with id {} try to choose {} as timeout".format(user_uuid, message.text))
        await message.answer(ERRORS['timeout_format'])
        return

@dp.message_handler(state=[BotStates.CHOOSE_SHILL_END[0]], chat_type=types.ChatType.PRIVATE)
async def choose_shill_end(message:types.Message):
    user_uuid = message.from_user.id
    state = dp.current_state(user=user_uuid)
    try:
        _, chat_uuid = await user_handler.get_user_with_chat(user_uuid)
        timeout = float(message.text)
        data = {'shill_end': timeout}
        await chat_handler.patch(chat_uuid, data)
        await message.answer(MESSAGES['choose_shill_end_success'].format(timeout))
        await state.set_state(BotStates.PENDING[0])
    except ValueError:
        log.error("User with id {} try to choose {} as end timeout".format(user_uuid, message.text))
        await message.answer(ERRORS['end_timeout_format'])
        return


# from here starts single commands

@dp.message_handler(state=[None, BotStates.PENDING[0]], commands=['choose_shill_message'], chat_type=types.ChatType.PRIVATE)
async def choose_shill_message_start(message:types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(BotStates.CHOOSE_SHILL_MESSAGE[0])
    await message.answer(MESSAGES['choose_shill_message'])

@dp.message_handler(state=[None, BotStates.PENDING[0]], commands=['choose_links'], chat_type=types.ChatType.PRIVATE)
async def choose_links_start(message:types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(BotStates.CHOOSE_LINKS[0])
    await message.answer(MESSAGES['choose_links'])

@dp.message_handler(state=[None, BotStates.PENDING[0]], commands=['choose_packs'], chat_type=types.ChatType.PRIVATE)
async def choose_packs_start(message:types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(BotStates.CHOOSE_PACKS[0])
    await choose_packs(message)

@dp.message_handler(state=[None, BotStates.PENDING[0]], commands=['choose_timeout'], chat_type=types.ChatType.PRIVATE)
async def choose_timeout_start(message:types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(BotStates.CHOOSE_TIMEOUT[0])
    await message.answer(MESSAGES['choose_timeout'])

@dp.message_handler(state=[None, BotStates.PENDING[0]], commands=['choose_shill_end'], chat_type=types.ChatType.PRIVATE)
async def choose_shill_end_start(message:types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(BotStates.CHOOSE_SHILL_END[0])
    await message.answer(MESSAGES['choose_shill_end'])

@dp.callback_query_handler(lambda callback: callback.data.startswith('pack'), state=BotStates.CHOOSE_PACKS[0])
async def choose_packs_finish(callback:types.CallbackQuery):
    user_uuid = callback.from_user.id
    pack_uuid = callback.data.replace('pack_', '')
    state = dp.current_state(user=user_uuid)
    try:
        _, chat_uuid = await user_handler.get_user_with_chat(user_uuid)
        pack = await packs_handler.get(pack_uuid)
        data = {'shill_links': pack['shill_links']}
        await chat_handler.patch(chat_uuid, data)
        await state.set_state(BotStates.PENDING[0])
        await callback.message.answer(MESSAGES['choose_packs_success'])
    except Exception as exc:
        exc = to_custom_exc(exc, user_uuid)
        log.error(exc.dev_message)
        await callback.message.answer(exc.user_message)
        await state.set_state(BotStates.PENDING[0])
    finally:
        await callback.answer()

@dp.message_handler(state=[BotStates.CHOOSE_LINKS[0]], chat_type=types.ChatType.PRIVATE)
async def choose_links(message:types.Message):
    user_uuid = message.from_user.id
    state = dp.current_state(user=user_uuid)
    await links(message)
    await state.set_state(BotStates.PENDING[0])

@dp.message_handler(state=[BotStates.CHOOSE_SHILL_MESSAGE[0]], chat_type=types.ChatType.PRIVATE)
async def choose_shill_message(message:types.Message):
    state = dp.current_state(user=message.from_user.id)
    await shill_message(message)
    await state.set_state(BotStates.PENDING[0])

@dp.message_handler(state=[BotStates.CHOOSE_TIMEOUT[0]], chat_type=types.ChatType.PRIVATE)
async def choose_timeout(message:types.Message):
    user_uuid = message.from_user.id
    state = dp.current_state(user=user_uuid)
    try:
        _, chat_uuid = await user_handler.get_user_with_chat(user_uuid)
        timeout = float(message.text)
        data = {'shill_timeout': int(timeout)}
        await chat_handler.patch(chat_uuid, data)
        await state.set_state(BotStates.PENDING[0])
        await message.answer(MESSAGES['choose_timeout_success'].format(int(timeout)))
    except ValueError:
        log.error("User with id {} try to choose {} as end timeout".format(user_uuid, message.text))
        await message.answer(ERRORS['end_timeout_format'])
        return

