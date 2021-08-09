from aiogram import types
from dispatcher import dp
from database import pg
import config as cfg

import lang

@dp.callback_query_handler(lambda call: "lang" in call.data)
async def langCallbacks(call: types.callback_query):
	chatLang = call.data.split('-')[1]
	pg.setChatLang(call.message.chat.id, chatLang)

	await call.message.edit_text(text=getattr(lang, chatLang).langChange)

@dp.callback_query_handler()
async def callbacks(call: types.callback_query):
	return