from aiogram import types
from dispatcher import dp
from database import pg
import config as cfg

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
	
	if call_data == "language":
		languageMarkup = types.InlineKeyboardMarkup(row_width=3)
		languageMarkup.add(
			types.InlineKeyboardButton(text="Русский", callback_data="language-ru_RU"),
			types.InlineKeyboardButton(text="English", callback_data="language-en_US"),
			types.InlineKeyboardButton(text="Укранська", callback_data="language-uk_UA")
		)
		
		await call.message.edit_reply_markup(reply_markup=languageMarkup)
	elif call_data == "max_warns":
		maxwarnsMarkup = types.InlineKeyboardMarkup(row_width=4)
		maxwarnsMarkup.add(
			types.InlineKeyboardButton(text="3", callback_data="max_warn-3"),
			types.InlineKeyboardButton(text="5", callback_data="max_warn-5"),
			types.InlineKeyboardButton(text="7", callback_data="max_warn-7"),
			types.InlineKeyboardButton(text="10", callback_data="max_warn-10")
		)
		maxwarnsMarkup.add(
			types.InlineKeyboardButton(text=getattr(lang, chatLang).backButtonText, callback_data="back-settings")
		)

		await call.message.edit_reply_markup(reply_markup=maxwarnsMarkup)

@dp.callback_query_handler(lambda call: "max_warn" == call.data.split('-')[0])
async def maxwarnsCallbacks(call: types.callback_query):
	chatLang = pg.getChatLang(call.message.chat.id)
	call_data = call.data.split('-')[1]

	return

@dp.callback_query_handler(lambda call: "back" == call.data.split('-')[0])
async def backCallbacks(call: types.callback_query):
	chatLang = pg.getChatLang(call.message.chat.id)
	call_data = call.data.split('-')[1]

	return

@dp.callback_query_handler(lambda call: "" == call.data.split('-')[0])
async def Callbacks(call: types.callback_query):
	chatLang = pg.getChatLang(call.message.chat.id)
	call_data = call.data.split('-')[1]

	return