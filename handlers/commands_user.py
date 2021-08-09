from aiogram import types
from dispatcher import dp
from database import pg
import config as cfg
import functions as fnc

import random

@dp.message_handler(lambda message: fnc.getCommand(message) in pg.getCommandsList(message.chat.id))
async def userCommand(message: types.Message):
	await message.reply(text=pg.getCommandOutput(message.chat.id, fnc.getCommand(message)), parse_mode="HTML")
