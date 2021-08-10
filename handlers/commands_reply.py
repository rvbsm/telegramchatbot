from aiogram import types
from dispatcher import dp
from database import pg
import config as cfg
import functions as fnc

import lang

@dp.message_handler(commands=["report"], is_reply=True)
async def userReport(message: types.Message):
	pg.updateUserCounter(message.from_user.id, message.chat.id)

	return