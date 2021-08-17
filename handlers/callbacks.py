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
		)
		)


@dp.callback_query_handler(lambda call: "maxwarn" == call.data.split('-')[0])
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