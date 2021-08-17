from aiogram import types
from aiogram.types.inline_keyboard import InlineKeyboardMarkup
from database import pg
import lang

def settingsMarkup(chatLang, message: types.Message) -> InlineKeyboardMarkup:
	settingsMarkup = types.InlineKeyboardMarkup(row_width=3)

	settingsMarkup.row(
		types.InlineKeyboardButton(callback_data="settings-language", text=getattr(lang, chatLang).settingsLangText),
		types.InlineKeyboardButton(callback_data="settings-maxwarns", text=getattr(lang, chatLang).settingsWarnText + str(pg.getChatMaxWarns(message.chat.id)))
	)
	settingsMarkup.row(
		types.InlineKeyboardButton(callback_data="settings-defaultchat", text=getattr(lang, chatLang).settingsChatDefaultsText),
		types.InlineKeyboardButton(callback_data="settings-defaultadmin", text=getattr(lang, chatLang).settingsAdminDefaultsText)
	)

	return settingsMarkup