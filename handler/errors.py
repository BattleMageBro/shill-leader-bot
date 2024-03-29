from aiogram import utils, types
from core import dp
from exceptions import to_custom_exc
from logg import log
from states import BotStates
from messages import ERRORS


#ToDo нужна обработка ошибки BotKicked типо бот был удален из группы, пожалуйста выберите другую группу /choose_chat или добавить бота обратно

@dp.errors_handler(exception=utils.exceptions.NetworkError)
async def network_main_error(update: types.Update, exception:utils.exceptions.NetworkError):
    log.error(exception)
    return True

@dp.errors_handler(exception=utils.exceptions.BotKicked)
async def bot_kicked_error(update: types.Update, exception:utils.exceptions.NetworkError):
    await update.message.answer(ERRORS['bot_kicked'])
    return True

@dp.errors_handler()
async def default_error_worker(update, exception):
    message = update.message
    user_uuid = message.from_user.id
    state = dp.current_state(user=user_uuid)
    exc = to_custom_exc(exception, message.from_user.id)
    log.error(exc.dev_message)
    await message.answer(exc.user_message)
    await state.set_state(BotStates.PENDING[0])
    return True