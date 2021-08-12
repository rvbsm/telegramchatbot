from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from dispatcher import bot
from config import botToken
from database import pg

class isAdminFilter(BoundFilter):
	key = "is_admin"

	def __init__(self, is_admin):
		self.is_admin = is_admin

	async def check(self, message: types.Message):
		return message.from_user.id in pg.getChatAdmins(message.chat.id)

class isBotFilter(BoundFilter):
	key = "is_bot"

	def __init__(self, is_bot):
		self.is_bot = is_bot

	async def check(self, message: types.Message):
		return message.new_chat_members[0].id == int(botToken.split(':')[0])

class isBotAdminFilter(BoundFilter):
	key = "is_bot_admin"

	def __init__(self, is_bot_admin):
		self.is_bot_admin = is_bot_admin

	async def check(self, message: types.Message):
		bot = await bot.get_chat_member(chat_id=message.chat.id, user_id=botToken.split(':')[0])
		return await bot.is_chat_admin()