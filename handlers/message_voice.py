from aiogram import types
from dispatcher import dp
from database import pg
import config as cfg

# ~
@dp.message_handler(content_types=["voice"])
async def voiceMessage(message: types.Message):
	print("melThrow")
