from aiogram import types
from core import dp, bot, postgres
from states import BotStates
from handler.utils import is_private
from messages import MESSAGES
from logg import log
from exceptions import UserError, to_custom_exc

@dp.message_handler(state=[BotStates.CHOOSE_CHAT[0]])
async def choose_chat(message:types.Message):
    await message.answer(MESSAGES['choose_chat'])
    await message.answer(MESSAGES['choose_options'])

async def shill_message(message:types.Message):
    user_id = message.from_user.id
    user = await postgres.select('users', 'user_uuid', user_id)
    log.debug(user)
    if type(user) == dict:
        user = user[0]
    else:
        user_message = str.format('Sorry user with your\'s id %s doesn\'t exist in our database.'
                                     'Please email to support.shill_leader@gmail.com we\'ll help you',
                                     user_id)
        dev_message = str.format('no user with id: %s', user_id)
        raise UserError(user_message=user_message, developer_message=dev_message)
    
    chat_uuid = user.get('current_chat')
    if not user.get('current_chat'):
        user_message = str.format('You have no choosen chat to work with.' 
                                  'Please type /choose_chat if you already added chats to ShillLeaderBot or add new chat')
        dev_message = str.format('user with id %s has no current_chat', user_id)
        raise UserError(user_message=user_message, developer_message=dev_message)

    shill_message = message.text
    data = {'shill_message': shill_message}
    await postgres.update('chat', 'chat_uuid', chat_uuid, data)
    await message.answer(MESSAGES['choose_shill_message_success'])

@dp.message_handler(state=[None, BotStates.PENDING[0]], commands=['choose_options'])
async def start_choosing_options(message:types.Message):
    user_id = message.from_user.id
    try:
        user = await postgres.select('users', 'user_uuid', message.from_user.id)
    except Exception as exc:
        exc = to_custom_exc(exc, user_id)
        log.error(exc.dev_message)
        await message.answer(exc.user_message)
        return
    #next step is choose shill message 
    #then links
    #then timeout   
    # ToDo : add packs

    state = dp.current_state(user=message.from_user.id)
    await state.set_state(BotStates.CHOOSE_SHILL_MESSAGE[0])
    await message.answer(MESSAGES['choose_options'])
    await message.answer(MESSAGES['choose_shill_message'])

@dp.message_handler(state=[BotStates.CHOOSE_SHILL_MESSAGE_OPTS[0]])
async def choose_shill_message_opts(message:types.Message):
    try:
        await shill_message(message)
    except Exception as exc:
        log.error(exc.dev_message)
        await message.answer(exc.user_message)
    
    state = dp.current_state(user=user_id)
    await state.set_state(BotStates.CHOOSE_LINKS_OPTS[0])
    await message.answer(MESSAGES['choose_links'])

@dp.message_handler(state=[BotStates.CHOOSE_SHILL_MESSAGE[0]])
async def choose_shill_message(message:types.Message):
    try:
        await shill_message(message)
    except Exception as exc:
        log.error(exc.dev_message)
        await message.answer(exc.user_message)

    state = dp.current_state(user=user_id)
    await state.set_state(BotStates.PENDING[0])


@dp.message_handler(state=[BotStates.CHOOSE_LINKS[0]])
async def choose_links_opts(message:types.Message):
    #toDo custom exceptions не работают пока что, надо вынести работу с чатами и юзерами в отдельный модуль и только тогда работать по человечески
    user_id = message.from_user.id
    user = await postgres.select('users', 'user_uuid', user_id)
    log.debug(user)
    if type(user) == dict:
        user = user[0]
    else:
        user_message = str.format('Sorry user with your\'s id %s doesn\'t exist in our database.'
                                     'Please email to support.shill_leader@gmail.com we\'ll help you',
                                     user_id)
        dev_message = str.format('no user with id: %s', user_id)
        raise UserError(user_message=user_message, developer_message=dev_message)
    
    chat_uuid = user.get('current_chat')
    if not user.get('current_chat'):
        user_message = str.format('You have no choosen chat to work with.' 
                                  'Please type /choose_chat if you already added chats to ShillLeaderBot or add new chat')
        dev_message = str.format('user with id %s has no current_chat', user_id)
        raise UserError(user_message=user_message, developer_message=dev_message)

    links = message.text.strip(' ').split(',')
    data = {'links': links}
    await postgres.update('chat', 'chat_uuid', chat_uuid, data)
    await message.answer(MESSAGES['choose_links_success'])

    state = dp.current_state(user=user_id)
    await state.set_state(BotStates.CHOOSE_TIMEOUT[0])
    await message.answer(MESSAGES['choose_timeout'])
