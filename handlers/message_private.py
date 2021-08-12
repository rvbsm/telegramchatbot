from aiogram import types
from dispatcher import dp
from database import pg
import config as cfg

# ~
@dp.message_handler(lambda message: message.from_user.id == message.chat.id, content_types=["any"])
async def privateMessage(message: types.Message):
	privateMarkup = types.InlineKeyboardMarkup(row_width=2)
	
	privateMarkup.row(
		types.InlineKeyboardButton(text="Добавить", url="t.me/vasyapipkinbot?startgroup=true"))
	privateMarkup.row(
		types.InlineKeyboardButton(text="Разработчик", url="tg://user?id=2006035302"),
		types.InlineKeyboardButton(text="Помощь", url="https://google.com"))
	
	await message.reply(text="Добавь меня в чат", reply_markup=privateMarkup)
