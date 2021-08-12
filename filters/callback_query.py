from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from config import botToken
from database import pg

class isAdminCallFilter(BoundFilter):
	key = "is_admin_call"

	def __init__(self, is_admin_call):
		self.is_admin_call = is_admin_call

	async def check(self, call: types.callback_query):
		return call.from_user.id in call.message.chat.get_administrators()