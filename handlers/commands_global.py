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

@dp.message_handler(commands=["addcom"], is_admin=True)
async def userCommandAdd(message: types.Message):
	chatLang = pg.getChatLang(message.chat.id)

	command = fnc.getCommandArgs(message)[0]
	commandOutput = ' '.join(fnc.getCommandArgs(message)[1:])

	if not command in pg.getCommandsList(message.chat.id):
		pg.addCommand(message.chat.id, command, commandOutput)
	else:
		pg.editCommand(message.chat.id, command, commandOutput)

	await message.reply(text=getattr(lang, chatLang).commandNewText + command)

@dp.message_handler(commands=["delcom"], is_admin=True)
async def userCommandRemove(message: types.Message):
	chatLang = pg.getChatLang(message.chat.id)

	command = fnc.getCommandArgs(message)[0]
	if command in pg.getCommandsList(message.chat.id):
		pg.removeCommand(message.chat.id, command)

		await message.reply(text=getattr(lang, chatLang).commandRemoveText + command)

@dp.message_handler(commands=["admin", "user"], is_admin=True, is_reply=True)
async def userPromote(message: types.Message):
	chatLang = pg.getChatLang(message.chat.id)

	if not pg.existUser(message.reply_to_message.from_user.id, message.chat.id):
		if message.reply_to_message.from_user.username:
			pg.addUser(message.reply_to_message.from_user.id, message.chat.id, message.reply_to_message.from_user.username)
		else:
			pg.addUser(message.reply_to_message.from_user.id, message.chat.id, message.reply_to_message.from_user.first_name)

	if fnc.getCommand(message) == "admin":
		if pg.getUserStatus(message.reply_to_message.from_user.id, message.chat.id):
			return

		pg.setUserStatus(message.reply_to_message.from_user.id, message.chat.id, True)
		await message.reply_to_message.reply(text=getattr(lang, chatLang).promoteToAdminText)
	elif fnc.getCommand(message) == "user":
		if not pg.getUserStatus(message.reply_to_message.from_user.id, message.chat.id):
			return

		pg.setUserStatus(message.reply_to_message.from_user.id, message.chat.id, False)
		await message.reply_to_message.reply(text=getattr(lang, chatLang).promoteToUserText)

@dp.message_handler(commands=["locale", "language"], is_admin=True)
async def chatLanguage(message: types.Message):
	return

@dp.message_handler(commands=["warn"], is_admin=True, is_reply=True)
async def adminWarn(message: types.Message):
	pg.addUserWarn(message.reply_to_message.from_user.id, message.chat.id)

@dp.message_handler(commands=["ban"], is_admin=True, is_reply=True)
async def adminBan(message: types.Message):
	return

@dp.message_handler(commands=["forgive"], is_admin=True, is_reply=True)
async def adminForgive(message: types.Message):
	pg.removeUserWarn(message.reply_to_message.from_user.id, message.chat.id)

@dp.message_handler(commands=["report"], is_reply=True)
async def userReport(message: types.Message):
	return

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