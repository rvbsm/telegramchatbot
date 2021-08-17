from aiogram import types
from dispatcher import dp
from database import pg
import config as cfg


@dp.message_handler(content_types=types.ContentType.TEXT, is_channel=True)
async def textMessage(message: types.Message):
	print(message)

# ~
@dp.message_handler(content_types=types.ContentType.TEXT)
async def textMessage(message: types.Message):
	if not pg.existUser(message.from_user.id, message.chat.id):
		if message.from_user.username:
			pg.addUser(message.from_user.id, message.chat.id, message.from_user.username)
		else:
			pg.addUser(message.from_user.id, message.chat.id, message.from_user.first_name)

	if message.from_user.username:
		pg.setUserName(message.from_user.id, message.chat.id, message.from_user.username)
	else:
		pg.setUserName(message.from_user.id, message.chat.id, message.from_user.first_name)

	pg.updateUserCounter(message.from_user.id, message.chat.id)

@dp.message_handler(content_types=types.ContentType.VOICE, is_channel=True)
async def voiceMessage(message: types.Message):
	return