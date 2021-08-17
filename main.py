from aiogram import executor
from dispatcher import dp, bot
from config import webhookUrl, webhookPath
import filters
import handlers

import logging
import os

logging.basicConfig(level=logging.INFO)

async def onStartUp(dp):
	await bot.delete_webhook(drop_pending_updates=True)
	await bot.set_webhook(webhookUrl, drop_pending_updates=True)


executor.start_webhook(dispatcher=dp, skip_updates=False, on_startup=onStartUp, webhook_path=webhookPath, host="0.0.0.0", port=os.getenv("PORT"))