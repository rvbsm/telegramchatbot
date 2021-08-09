from aiogram import types
from dispatcher import dp
from database import pg
import config as cfg

@dp.callback_query_handler()
async def callbacks(call: types.callback_query):
	return