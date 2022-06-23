from aiogram import types
from core import dp, bot
import os, time
import datetime
from messages import MESSAGES
from states import BotStates
import asyncio
from handler import utils
from logg import logger

SHILL_MESSAGE = ['3', '2', '1']


# ------------------------ for tests -----------------------------

@dp.message_handler(state=[None], commands='test1')
async def test_handler(message: types.Message):
    if not utils.is_private(message.chat.type):
        return
    logger.debug(f'hey we have message {message}')
    await message.reply("Тёмчик твой тест успешен!)")

# ------------------------ end for tests -----------------------------

@dp.message_handler(state='*', commands=['setstate'])
async def process_setstate_command(message: types.Message):
    if not utils.is_private(message.chat.type):
        return
    argument = message.get_args()
    state = dp.current_state(user=message.from_user.id)
    if not argument:
        await state.reset_state()
        return await message.reply(MESSAGES['stateReset'])

    if (not argument.isdigit()) or (not int(argument) < len(BotStates.all())):
        return await message.reply(MESSAGES['invalidKey'].format(key=argument))

    await state.set_state(BotStates.all()[int(argument)])
    await message.reply(MESSAGES['stateChange'], reply=False)


@dp.message_handler(state=[None, BotStates.PENDING[0]], commands=['help'])
async def help_case(message: types.Message):
    if not utils.is_private(message.chat.type):
        return
    await message.answer(MESSAGES['help'])

@dp.message_handler(state=[None, BotStates.PENDING[0]], commands=['start_shilling'])
async def start_shilling(message: types.Message):
    if not utils.is_private(message.chat.type):
        return
    end_time = datetime.datetime.now().timestamp() + 60
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(BotStates.START_SHILLING[0])
    await message.answer(MESSAGES['startShilling'])

@dp.message_handler(state=[BotStates.START_SHILLING[0]])
async def start_shill(message: types.Message):
    if not utils.is_private(message.chat.type):
        return
    logger.debug(message)
    SHILL_MESSAGE.append(message.text)
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(BotStates.SHILLING[0])
    await message.answer(MESSAGES['shillOptsChoosen'])

@dp.message_handler(state=[BotStates.SHILLING[0]], commands=['start'])
async def shilling(message: types.Message):
    if not utils.is_private(message.chat.type):
        return
    logger.debug(message)
    state = dp.current_state(user=message.from_user.id)
    end_time = datetime.datetime.now().timestamp() + 20
    while datetime.datetime.now().timestamp() < end_time:
        for item in SHILL_MESSAGE:
            await bot.send_message(chat_id=message.chat.id, text=item)
            await asyncio.sleep(1)
        await asyncio.sleep(5)
    await state.set_state(BotStates.PENDING[0])
    await message.answer(MESSAGES['shillEnds'])

@dp.message_handler(state=[None, BotStates.PENDING])
async def first_test_state_case_met(message: types.Message):
    if not utils.is_private(message.chat.type):
        return
    logger.debug(message)
    await message.reply('мы на самом старте!', reply=False)

@dp.message_handler(state=BotStates.all())
async def some_test_state_case_met(message: types.Message):
    if not utils.is_private(message.chat.type):
        return
    text = 'wtf noone catch this before'
    await message.reply(text, reply=False)
