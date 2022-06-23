from aiogram import types
from core import dp, bot, postgres
from states import BotStates
from handler.utils import is_private
from messages import MESSAGES
from logg import logger
from exceptions import UserError

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
        user_message = 'Sorry user with your\'s id doesn\'t exist in our database. Please email to support.shill_leader@gmail.com we\'ll help you'
        dev_message = string.format('no user with id: %s', user_id)
        raise UserError(user_message=user_message, developer_message=dev_message)
    
    chat_uuid = user.get('current_chat')
    if not user.get('current_chat'):
        user_message = 'You have no choosen chat to work with. Please type /choose_chat if you already added chats to ShillLeaderBot or add new chat'
        dev_message = string.format('user with id %s has no current_chat', user_id)
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
        await message.answer(exc.user_message)
        return
    #нет необходимости тут дергать чаты
    #chat = await postgres.select('chat', 'chat_uuid', user['current_chat'])[0]

    #next step is choose shill message 
    #then links
    #then timeout   
    # ToDo : add packs

    state = dp.current_state(user=message.from_user.id)
    await state.set_state(BotStates.CHOOSE_SHILL_MESSAGE[0])
    await message.answer(MESSAGES['choose_options'])
    await message.answer(MESSAGES['choose_shill_message'])

@dp.message_handler(state=[BotStates.CHOOSE_SHILL_MESSAGE_OPTS[0]])
async def choose_shill_message(message:types.Message):
    try:
        await shill_message(message)
    except Exception as exc:
        err = string.format('Choose Shill Message failed with %s error: %s', exc.error_code, exc.message)
        message.answer(exc.user_message)
    
    state = dp.current_state(user=user_id)
    await state.set_state(BotStates.CHOOSE_LINKS_OPTS[0])
    await message.answer(MESSAGES['choose_links'])

@dp.message_handler(state=[BotStates.CHOOSE_SHILL_MESSAGE[0]])
async def choose_shill_message(message:types.Message):
    try:
        await shill_message(message)
    except Exception as exc:
        err = string.format('Choose Shill Message failed with %s error: %s', exc.error_code, exc.message)
        message.answer(exc.user_message)

    state = dp.current_state(user=user_id)
    await state.set_state(BotStates.PENDING[0])


@dp.message_handler(state=[BotStates.CHOOSE_LINKS[0]])
async def choose_links(message:types.Message):
    pass

