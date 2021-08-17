from aiogram import types
from dispatcher import dp
from database import pg
import functions.command as cmd
import functions.markup as markup
import lang

import datetime

@dp.message_handler(commands=["addcom"], is_admin=True)
async def userCommandAdd(message: types.Message):
	chatLang = pg.getChatLang(message.chat.id)

	command = cmd.getCommandArgs(message)[0]
	commandOutput = ' '.join(cmd.getCommandArgs(message)[1:])

	if not command in pg.getCommandsList(message.chat.id):
		pg.addCommand(message.chat.id, command, commandOutput)
	else:
		pg.editCommand(message.chat.id, command, commandOutput)

	await message.reply(text=getattr(lang, chatLang).commandNewText + command)

@dp.message_handler(commands=["delcom"], is_admin=True)
async def userCommandRemove(message: types.Message):
	pg.updateUserCounter(message.from_user.id, message.chat.id)

	chatLang = pg.getChatLang(message.chat.id)

	command = cmd.getCommandArgs(message)[0]
	if command in pg.getCommandsList(message.chat.id):
		pg.removeCommand(message.chat.id, command)

		await message.reply(text=getattr(lang, chatLang).commandRemText + command)

# ~
@dp.message_handler(commands=["admin", "user"], is_admin=True, is_reply=True, bot_promote=True)
async def userPromote(message: types.Message):
	pg.updateUserCounter(message.from_user.id, message.chat.id)

	chatLang = pg.getChatLang(message.chat.id)

	if not pg.existUser(message.reply_to_message.from_user.id, message.chat.id):
		if message.reply_to_message.from_user.username:
			pg.addUser(message.reply_to_message.from_user.id, message.chat.id, message.reply_to_message.from_user.username)
		else:
			pg.addUser(message.reply_to_message.from_user.id, message.chat.id, message.reply_to_message.from_user.first_name)

	if cmd.getCommand(message) == "admin":
		if pg.getUserStatus(message.reply_to_message.from_user.id, message.chat.id):
			return

		await message.chat.promote(
			user_id=message.reply_to.message.from_user.id,
			can_change_info=True,
			can_delete_messages=True,
			can_pin_messages=True
		)

		pg.setUserStatus(message.reply_to_message.from_user.id, message.chat.id, True)
		await message.reply_to_message.reply(text=getattr(lang, chatLang).promoteToAdminText)
	elif cmd.getCommand(message) == "user":
		if not pg.getUserStatus(message.reply_to_message.from_user.id, message.chat.id):
			return

		await message.chat.restrict(
			user_id=message.reply_to.message.from_user.id,
			can_send_messages=True
		)
		pg.setUserStatus(message.reply_to_message.from_user.id, message.chat.id, False)
		await message.reply_to_message.reply(text=getattr(lang, chatLang).promoteToUserText)

@dp.message_handler(commands=["locale", "language", "lang"], is_admin=True)
async def chatLanguage(message: types.Message):
	pg.updateUserCounter(message.from_user.id, message.chat.id)

	chatLang = pg.getChatLang(message.chat.id)

	languageMarkup = types.InlineKeyboardMarkup(row_width=3)
	languageMarkup.add(
		types.InlineKeyboardButton(text="Русский", callback_data="language-ru_RU"),
		types.InlineKeyboardButton(text="English", callback_data="language-en_US"),
		types.InlineKeyboardButton(text="Укранська", callback_data="language-uk_UA")
	)

	await message.reply(text="Выбор языка\t/\tLanguage choice\t/\tВыбір мови", reply_markup=languageMarkup)

@dp.message_handler(commands=["warn"], is_admin=True, is_reply=True)
async def adminWarn(message: types.Message):
	chatLang = pg.getChatLang(message.chat.id)
	pg.updateUserCounter(message.from_user.id, message.chat.id)

	pg.addUserWarn(message.reply_to_message.from_user.id, message.chat.id)
	await message.reply_to_message.reply(getattr(lang, chatLang).warnAddText.format(pg.getUserWarn(message.from_user.id, message.chat.id), pg.getChatMaxWarns(message.chat.id)))

	if pg.getUserWarn(message.from_user.id, message.chat.id) == pg.getChatMaxWarns(message.chat.id):
		await adminBan(message)

# ~
@dp.message_handler(commands=["ban"], is_admin=True, is_reply=True, bot_ban=True)
async def adminBan(message: types.Message):
	chatLang = pg.getChatLang(message.chat.id)
	pg.updateUserCounter(message.from_user.id, message.chat.id)

	await message.reply(text=getattr(lang, chatLang).banText)
	message.chat.kick(user_id=message.reply_to.message.from_user.id)

@dp.message_handler(commands=["unban", "pardon"], is_admin=True, is_reply=True, bot_ban=True)
async def adminPardon(message: types.Message):
	chatLang = pg.getChatLang(message.chat.id)
	pg.updateUserCounter(message.from_user.id, message.chat.id)

	pg.removeUserWarn(message.reply_to.message.from_user.id, message.chat.id)
	await message.chat.unban(message.reply_to.message.from_user.id, True)
	
	await message.reply_to_message.reply(text=getattr(lang, chatLang).warnRemText)

# ~
@dp.message_handler(commands=["settings"], is_admin=True)
async def settingsMessage(message: types.Message):
	chatLang = pg.getChatLang(message.chat.id)

	settingsMarkup = types.InlineKeyboardMarkup(row_width=3)
	settingsMarkup.add(
		types.InlineKeyboardButton(text=getattr(lang, chatLang).settingsLangText, callback_data="settings-language"),
		types.InlineKeyboardButton(text=getattr(lang, chatLang).settingsWarnText + pg.getChatMaxWarns(message.chat.id), callback_data="settings-max_warns")
		#types.InlineKeyboardButton(text=getattr(lang, chatLang).settingsDefault Text, callback_data="settings-")
	)

	await message.reply(text=getattr(lang, chatLang).settingsTitle, reply_markup=settingsMarkup)