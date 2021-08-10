from aiogram import types, executor
from dispatcher import bot, dp
import handlers

import logging, requests, os

import config as cfg
from database import DataBase
import functions as fnc

logging.basicConfig(level=logging.INFO)

#
#	Настройки чата:
#		Рандомный шип:				Да/Нет
#	Баны и репорты
#	Рандомный шип
#	Пасхалки
#

async def onStartUp(dp):
	await bot.delete_webhook(drop_pending_updates=True)
	await bot.set_webhook(cfg.webhookUrl, drop_pending_updates=True)


executor.start_webhook(dispatcher=dp, skip_updates=False, on_startup=onStartUp, webhook_path=cfg.webhookPath, host="0.0.0.0", port=os.getenv("PORT"))