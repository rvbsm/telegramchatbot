from aiogram import types
from dispatcher import dp
from database import pg
import config as cfg
import functions.command as cmd

@dp.message_handler(lambda message: cmd.getCommand(message) in pg.getCommandsList(message.chat.id))
async def userCommand(message: types.Message):
	await message.reply(text=pg.getCommandOutput(message.chat.id, cmd.getCommand(message)), parse_mode="HTML")
