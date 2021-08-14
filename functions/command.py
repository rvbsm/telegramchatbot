from aiogram import types

def getCommandAll(message: types.Message):
	"""
	return: Returns List if command
	rtype: `list`
	"""
	if message.text[0] in ('/', '!'):
		return message.text.split()
	else:
		return message.text

def getCommand(message: types.Message):
	"""
	return: Returns command without command-prefix
	rtype: `str`
	"""
	return getCommandAll(message)[0][1:]

def getCommandArgs(message: types.Message):
	"""
	return: Returns List with arguments of command
	rtype: `list`
	"""
	return getCommandAll(message)[1:]