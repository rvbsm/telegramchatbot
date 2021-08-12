from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from dispatcher import bot
from config import botToken
from database import pg

class canBotChangeFilter(BoundFilter):
	key = "bot_change"

	def __init__(self, bot_change):
		self.bot_change = bot_change

	async def check(self, message: types.Message):
		bot_member = await bot.get_chat_member(chat_id=message.chat.id, user_id=botToken.split(':')[0])
		return bot_member.can_change_info

class canBotDeleteFilter(BoundFilter):
	key = "bot_delete"

	def __init__(self, bot_delete):
		self.bot_delete = bot_delete

	async def check(self, message: types.Message):
		bot_member = await bot.get_chat_member(chat_id=message.chat.id, user_id=botToken.split(':')[0])
		return bot_member.can_delete_message

class canBotBanFilter(BoundFilter):
	key = "bot_ban"

	def __init__(self, bot_ban):
		self.bot_ban = bot_ban

	async def check(self, message: types.Message):
		bot_member = await bot.get_chat_member(chat_id=message.chat.id, user_id=botToken.split(':')[0])
		return bot_member.can_restrict_members

class canBotPromoteFilter(BoundFilter):
	key = "bot_promote"

	def __init__(self, bot_promote):
		self.bot_promote = bot_promote

	async def check(self, message: types.Message):
		bot_member = await bot.get_chat_member(chat_id=message.chat.id, user_id=botToken.split(':')[0])
		return bot_member.can_promote_members
"""
user: {"id": id, "is_bot": bool, "first_name": name, "username": name}
"status": "administrator"
"can_be_edited":			bool
"can_manage_chat":			bool
"can_change_info":			bool
"can_delete_messages":		bool
"can_invite_users":			bool
"can_restrict_members":		bool
"can_pin_messages":			bool
"can_promote_members":		bool
"can_manage_voice_chats":	bool
"is_anonymous":				bool
"""