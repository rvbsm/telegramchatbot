from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from dispatcher import bot
from config import botToken
from database import pg

class isAdminFilter(BoundFilter):
	"""
	Check if the user is admin of chat
	return: Returns True if user is admin of chat
	rtype: `bool`
	"""
	key = "is_admin"

	def __init__(self, is_admin):
		self.is_admin = is_admin

	async def check(self, message: types.Message):
		admins = await message.chat.get_administrators()
		adminsList = set()
		for i in admins:
			adminsList.add(i.user.id)

		return message.from_user.id in adminsList

class isBotFilter(BoundFilter):
	"""
	Check if the user is current bot
	return: Returns True if bot
	rtype: `bool`
	"""
	key = "is_bot"

	def __init__(self, is_bot):
		self.is_bot = is_bot

	async def check(self, message: types.Message):
		return message.new_chat_members[0].id == int(botToken.split(':')[0])

class isBotAdminFilter(BoundFilter):
	"""
	Check if the bot is admin of chat
	return: Returns True if bot is admin of chat
	rtype: `bool`
	"""
	key = "is_bot_admin"

	def __init__(self, is_bot_admin):
		self.is_bot_admin = is_bot_admin

	async def check(self, message: types.Message):
		bot = await bot.get_chat_member(chat_id=message.chat.id, user_id=botToken.split(':')[0])
		return await bot.is_chat_admin()

class isChannelFilter(BoundFilter):
	key = "is_channel"

	def __init__(self, is_channel):
		self.is_channel = is_channel

	async def check(self, message: types.Message):
		if message.from_user.id == 777000:
			return message.sender_chat.type == "channel"
		else:
			return False