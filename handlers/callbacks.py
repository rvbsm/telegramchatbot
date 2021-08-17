from aiogram import types
from dispatcher import dp
from database import pg
import functions.markup as markup
import json

import lang

@dp.callback_query_handler(lambda call: "language" == call.data.split('-')[0])
async def langCallbacks(call: types.callback_query):
	chatLang = call.data.split('-')[1]
	pg.setChatLang(call.message.chat.id, chatLang)

	await call.message.edit_text(text=getattr(lang, chatLang).langChange)

@dp.callback_query_handler(lambda call: "settings" == call.data.split('-')[0])
async def settingsCallbacks(call: types.callback_query):
	chatLang = pg.getChatLang(call.message.chat.id)
	call_data = call.data.split('-')[1]
	settingsMarkup = types.InlineKeyboardMarkup()

	if call_data == "language":
		settingsMarkup.add(
			types.InlineKeyboardButton(callback_data="language-ru_RU", text="Русский"),
			types.InlineKeyboardButton(callback_data="language-en_US", text="English"),
			types.InlineKeyboardButton(callback_data="language-uk_UA", text="Укранська")
		)
	elif call_data == "maxwarns":
		settingsMarkup.add(
			types.InlineKeyboardButton(callback_data="maxwarn-3", text="3"),
			types.InlineKeyboardButton(callback_data="maxwarn-5", text="5"),
			types.InlineKeyboardButton(callback_data="maxwarn-7", text="7"),
			types.InlineKeyboardButton(callback_data="maxwarn-10", text="10")
		)
	elif call_data == "defaultchat":
		settingsMarkup.add(
			types.InlineKeyboardButton(callback_data="defaultchat-can_send_messages", text=getattr(lang, chatLang).defaultchatSendMessage),
			types.InlineKeyboardButton(callback_data="defaultchat-can_send_media_messages", text=getattr(lang, chatLang).defaultchatSendMedia),
			types.InlineKeyboardButton(callback_data="defaultchat-can_send_polls", text=getattr(lang, chatLang).defaultchatSendPolls),
			types.InlineKeyboardButton(callback_data="defaultchat-can_send_other_messages", text=getattr(lang, chatLang).defaultchatSendOther),
			types.InlineKeyboardButton(callback_data="defaultchat-can_add_web_page_previews", text=getattr(lang, chatLang).defaultchatAddPreview),
			types.InlineKeyboardButton(callback_data="defaultchat-can_change_info", text=getattr(lang, chatLang).defaultchatChangeInfo),
			types.InlineKeyboardButton(callback_data="defaultchat-can_invite_users", text=getattr(lang, chatLang).defaultchatCanInvite),
			types.InlineKeyboardButton(callback_data="defaultchat-can_pin_messages", text=getattr(lang, chatLang).defaultchatPinMessages)
		)

	elif call_data == "defaultadmin":
		settingsMarkup.add(
			types.InlineKeyboardButton(callback_data="defaultadmin-is_anonymous", text=getattr(lang, chatLang).defaultadminIsAnonymous),
			types.InlineKeyboardButton(callback_data="defaultadmin-can_change_info", text=getattr(lang, chatLang).defaultadminCanChange),
			types.InlineKeyboardButton(callback_data="defaultadmin-can_delete_messages", text=getattr(lang, chatLang).defaultadminCanDelete),
			types.InlineKeyboardButton(callback_data="defaultadmin-can_invite_users", text=getattr(lang, chatLang).defaultadminCanInvite),
			types.InlineKeyboardButton(callback_data="defaultadmin-can_restrict_members", text=getattr(lang, chatLang).defaultadminCanRestrict),
			types.InlineKeyboardButton(callback_data="defaultadmin-can_pin_messages", text=getattr(lang, chatLang).defaultadminCanPin),
			types.InlineKeyboardButton(callback_data="defaultadmin-can_promote_members", text=getattr(lang, chatLang).defaultadminCanPromote)
		)
	settingsMarkup.add(
		types.InlineKeyboardButton(text=getattr(lang, chatLang).backButtonText, callback_data="back-settings")
	)
	await call.message.edit_reply_markup(reply_markup=settingsMarkup)
	await call.answer(show_alert=False)

@dp.callback_query_handler(lambda call: "defaultchat" == call.data.split('-')[0])
async def deafultChatCallbacks(call: types.callback_query):
	chatLang = pg.getChatLang(call.message.chat.id)
	call_data = call.data.split('-')[1]
	curSettings = pg.getChatSettings(call.message.chat.id)

	curSettings[call_data] = not curSettings[call_data]
	pg.updateChatSettings(json.dumps(curSettings))
	
	curSettings = types.ChatPermissions(**curSettings)
	
	await call.message.chat.set_permissions(permissions=curSettings)

@dp.callback_query_handler(lambda call: "defaultadmin" == call.data.split('-')[0])
async def defaultAdminCallbacks(call: types.callback_query):
	chatLang = pg.getChatLang(call.message.chat.id)
	call_data = call.data.split('-')[1]
	curSettings = pg.getAdminSettings(call.message.chat.id)
	curSettings[call_data] = not curSettings[call_data]
	pg.updateAdminSettings(call.message.chat.id, json.dumps(curSettings))

@dp.callback_query_handler(lambda call: "maxwarn" == call.data.split('-')[0])
async def maxwarnsCallbacks(call: types.callback_query):
	chatLang = pg.getChatLang(call.message.chat.id)
	call_data = call.data.split('-')[1]

	return

@dp.callback_query_handler(lambda call: "back" == call.data.split('-')[0])
async def backCallbacks(call: types.callback_query):
	chatLang = pg.getChatLang(call.message.chat.id)
	call_data = call.data.split('-')[1]
	settingsMarkup = types.InlineKeyboardMarkup()

	if call_data == "settings":
		await call.message.edit_reply_markup(reply_markup=markup.settingsMarkup(chatLang, call.message))
	return

@dp.callback_query_handler(lambda call: "" == call.data.split('-')[0])
async def Callbacks(call: types.callback_query):
	chatLang = pg.getChatLang(call.message.chat.id)
	call_data = call.data.split('-')[1]

	return