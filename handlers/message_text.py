from aiogram import types
from dispatcher import dp
from database import pg
import config as cfg

@dp.message_handler()
async def textMessage(message: types.Message):
	if not pg.existUser(message.from_user.id, message.chat.id):
		if message.from_user.username:
			pg.addUser(message.from_user.id, message.chat.id, message.from_user.username)
		else:
			pg.addUser(message.from_user.id, message.chat.id, message.from_user.first_name)

	if message.from_user.username:
		pg.updateUserName(message.from_user.id, message.chat.id, message.from_user.username)
	else:
		pg.updateUserName(message.from_user.id, message.chat.id, message.from_user.first_name)

	pg.updateUserCounter(message.from_user.id, message.chat.id)