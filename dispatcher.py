from aiogram import Bot, Dispatcher
from config import botToken

bot = Bot(token=botToken, parse_mode="HTML")
dp = Dispatcher(bot)