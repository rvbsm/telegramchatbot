from aiogram import types
import xml.etree.ElementTree as XmlElementTree
import httplib2, uuid, subprocess, tempfile, os

from config import yandexToken

def getCommandAll(message: types.Message):
	if message.text[0] in ('/', '!'):
		return message.text.split()
	else:
		return message.text

def getCommand(message: types.Message):
	return getCommandAll(message)[0][1:]

def getCommandArgs(message: types.Message):
	return getCommandAll(message)[1:]
