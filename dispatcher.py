from aiogram import Bot, Dispatcher
from filters import isOwnerFilter, isAdminFilter, isBotFilter

from config import botToken

bot = Bot(token=botToken, parse_mode="HTML")
dp = Dispatcher(bot)

dp.filters_factory.bind(isOwnerFilter)
dp.filters_factory.bind(isAdminFilter)
dp.filters_factory.bind(isBotFilter)