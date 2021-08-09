from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from config import botToken
from database import pg

class isOwnerFilter(BoundFilter):
	key = "is_owner"

	def __init__(self, is_owner):
		self.is_owner = is_owner

	async def check(self, message: types.Message):
		return message.from_user.id == 200635302

class isAdminFilter(BoundFilter):
	key = "is_admin"

	def __init__(self, is_admin):
		self.is_admin = is_admin

	async def check(self, message: types.Message):
		return pg.getUserStatus(message.from_user.id, message.chat.id)

class isBotFilter(BoundFilter):
	key = "is_bot"

	def __init__(self, is_bot):
		self.is_bot = is_bot

	async def check(self, message: types.Message):
		return message.new_chat_members[0].id == int(botToken.split(':')[0])