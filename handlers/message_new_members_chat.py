from aiogram import types
from dispatcher import dp
from database import pg
import config as cfg

import lang

@dp.message_handler(content_types=["new_chat_members"], is_bot=True)
async def addBotToChat(message: types.Message):
	pg.createTables(message["from"].id, message.chat.id, message.chat.title, message.message_id)

	chatLang = pg.getChatLang(message.chat.id)
	await message.reply(getattr(lang, chatLang).firstMessageText)

@dp.message_handler(content_types=["new_chat_members"])
async def addUserToChat(message: types.Message):
	if not pg.existUser(message.from_user.id, message.chat.id):
		if message.from_user.username:
			pg.addUser(message.from_user.id, message.chat.id, message.from_user.username)
		else:
			pg.addUser(message.from_user.id, message.chat.id, message.from_user.first_name)