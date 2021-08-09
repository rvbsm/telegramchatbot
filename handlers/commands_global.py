from aiogram import types
from dispatcher import dp
from database import pg
import config as cfg
import functions as fnc

import lang

@dp.message_handler(commands=["help"])
async def helpMessage(message: types.Message):
	chatLang = pg.getChatLang(message.chat.id)

	if pg.getCommandsList(message.chat.id):
		await message.reply(text=getattr(lang, chatLang).helpCommandsText + '\n!'.join(pg.getCommandsList(message.chat.id)))
	else:
		await message.reply(text=getattr(lang, chatLang).helpNoCommandsText)


@dp.message_handler(commands=["stat"])#, is_reply)
async def userStats(message: types.Message):
	chatLang = pg.getChatLang(message.chat.id)
	pg.getUserWarn(message.from_user.id, message.chat.id)
	await message.reply(text=getattr(lang, chatLang).aboutUserText.format(
		message.from_user.first_name,
		message.from_user.id,
		pg.getUserCounter(message.from_user.id, message.chat.id),
		pg.getUserWarn(message.from_user.id, message.chat.id),
		pg.getChatMaxWarns(message.chat.id)))