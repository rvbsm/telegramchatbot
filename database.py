import psycopg2
import config as cfg

class DataBase:
	def __init__(self, path):
		self.conn = psycopg2.connect(path, keepalives=1, keepalives_idle=300, keepalives_interval=60, keepalives_count=30)
		self.curs = self.conn.cursor()
		self.conn.autocommit = True

	def createTables(self, user_id: int, chat_id: int, chat_title: str, counter: int) -> None:
		"""
		Creates tables '<chat.id>_users' (and adds the user to it, admin=true),
		'chats_commands' and 'chats_settings'
		return: None
		rtype: `NoneType`
		"""
		self.curs.execute('''CREATE TABLE IF NOT EXISTS "%s_users" (
			"id" serial PRIMARY KEY NOT NULL,
			"name" text,
			"admin" bool DEFAULT false,
			"warn" smallint DEFAULT 0,
			"msg_counter" integer DEFAULT 0
		)''', (chat_id,))
		self.curs.execute('''INSERT INTO "%s_users"("id", "admin") VALUES(%s, %s) ON CONFLICT ("id") DO UPDATE SET "admin" = true''', (chat_id, user_id, True))

		self.curs.execute('''CREATE TABLE IF NOT EXISTS "chats_commands" (
			"id" bigint PRIMARY KEY NOT NULL,
			"command" text,
			"output" text
		)''')

		self.curs.execute('''CREATE TABLE IF NOT EXISTS "chats_settings" (
			"id" bigint PRIMARY KEY NOT NULL,
			"title" text NOT NULL,
			"members" integer,
			"max_warns" smallint DEFAULT 3,
			"msg_counter" integer DEFAULT 0,
			"lang" text DEFAULT 'ru_RU',
			"admin_defaults" json DEFAULT '{"is_anonymous": false, "can_change_info": true, "can_delete_messages": true, "can_invite_users": true, "can_restrict_members": true, "can_pin_messages": true, "can_promote_members": false}',
			"chat_defaults" json DEFAULT '{"can_send_messages": true, "can_send_media_messages": true, "can_send_polls": true, "can_send_other_messages": true, "can_add_web_page_previews": true, "can_change_info": true, "can_invite_users": true, "can_pin_messages": true}'
		)''')
		self.curs.execute('''INSERT INTO "chats_settings"("id", "title", "msg_counter") VALUES(%s, %s, %s) ON CONFLICT ("id") DO NOTHING''', (chat_id, chat_title, counter))


	def getUsers(self, chat_id: int) -> list[int]:
		"""
		return: Returns ist with user_id from chat
		rtype: `list`
		"""
		self.curs.execute('''SELECT "id" FROM "%s_users"''', (chat_id,))
		rows = self.curs.fetchall()
		for r in rows:
			return[r[0] for r in rows]

	def existUser(self, user_id: int, chat_id: int) -> bool:
		"""
		return: Returns True if user_id is in the table
		rtype: `bool`
		"""
		self.curs.execute('''SELECT * FROM "%s_users" WHERE "id" = %s''', (chat_id, user_id))
		result = self.curs.fetchall()
		return bool(len(result))

	def addUser(self, user_id: int, chat_id: int, username: str) -> None:
		"""
		Insert into table user_id, chat and username of user
		return: None
		rtype: `NoneType`
		"""
		self.curs.execute('''INSERT INTO "%s_users"("id", "name") VALUES(%s, %s) ON CONFLICT ("id") DO NOTHING''', (chat_id, user_id, username))

	def setUserName(self, user_id: int, chat_id: int, username: str) -> None:
		"""
		Updating username
		return: None
		rtype: `NoneType`
		"""
		self.curs.execute('''UPDATE "%s_users" SET "name" = %s WHERE "id" = %s''', (chat_id, username, user_id))


	def getUserStatus(self, user_id: int, chat_id: int) -> bool:
		"""
		return: Returns True if user is admin of this chat, otherwise False
		rtype: `bool`
		"""
		self.curs.execute('''SELECT "admin" FROM "%s_users" WHERE "id" = %s''', (chat_id, user_id))
		result = self.curs.fetchall()
		for r in result:
			return r[0]

	def setUserStatus(self, user_id: int, chat_id: int, status: bool) -> None:
		"""
		
		return: None
		rtype: `NoneType`
		"""
		self.curs.execute('''UPDATE "%s_users" SET "admin" = %s WHERE "id" = %s''', (chat_id, status, user_id))


	def getUserCounter(self, user_id: int, chat_id: int) -> int:
		self.curs.execute('''SELECT "msg_counter" FROM "%s_users" WHERE "id" = %s''', (chat_id, user_id))
		result = self.curs.fetchall()
		for r in result:
			return r[0]

	def updateUserCounter(self, user_id: int, chat_id: int) -> None:
		counter = self.getUserCounter(user_id, chat_id) + 1
		self.curs.execute('''UPDATE "%s_users" SET "msg_counter" = %s WHERE "id" = %s''', (chat_id, counter, user_id))


	def getUserWarn(self, user_id: int, chat_id: int) -> int:
		self.curs.execute('''SELECT "warn" FROM "%s_users" WHERE "id" = %s''', (chat_id, user_id))
		result = self.curs.fetchall()
		for r in result:
			return r[0]

	def addUserWarn(self, user_id: int, chat_id: int) -> None:
		warn = self.getUserWarn(user_id, chat_id) + 1
		self.curs.execute('''UPDATE "%s_users" SET "warn" = %s WHERE "id" = %s''', (chat_id, warn, user_id))

	def removeUserWarn(self, user_id: int, chat_id: int) -> None:
		self.curs.execute('''UPDATE "%s_users" SET "warn" = 0 WHERE "id" = %s''', (chat_id, user_id))


	def getCommandsList(self, chat_id: int) -> list[str]:
		self.curs.execute('''SELECT "command" FROM "chats_commands" WHERE "id" = %s''', (chat_id,))
		rows = self.curs.fetchall()
		
		if rows == []:
			return rows
		else:
			for r in rows:
				return[r[0] for r in rows]

	def getCommandOutput(self, chat_id: int, command: str) -> str:
		self.curs.execute('''SELECT "output" FROM "chats_commands" WHERE "command" = %s AND "id" = %s''', (command, chat_id))
		result = self.curs.fetchall()
		for r in result:
			return r[0]

	def addCommand(self, chat_id: int, command: str, output: str) -> None:
		self.curs.execute('''INSERT INTO "chats_commands"("id", "command", "output") VALUES(%s, %s, %s)''', (chat_id, command, output))

	def editCommand(self, chat_id: int, command: str, output: str) -> None:
		self.curs.execute('''UPDATE "chats_commands" SET "output" = %s WHERE "id" = %s AND "command" = %s''', (output, chat_id, command))

	def removeCommand(self, chat_id: int, command: str) -> None:
		self.curs.execute('''DELETE FROM "chats_commands" WHERE "id" = %s AND "command" = %s''', (chat_id, command))


	def getChatLang(self, chat_id: int) -> str:
		self.curs.execute('''SELECT "lang" FROM "chats_settings" WHERE "id" = %s''', (chat_id,))
		result = self.curs.fetchall()
		for r in result:
			return r[0]

	def setChatLang(self, chat_id: int, lang: str) -> None:
		self.curs.execute('''UPDATE "chats_settings" SET "lang" = %s WHERE "id" = %s''', (lang, chat_id))


	def getChatMaxWarns(self, chat_id: int) -> int:
		self.curs.execute('''SELECT "max_warns" FROM "chats_settings" WHERE "id" = %s''', (chat_id,))
		result = self.curs.fetchall()
		for r in result:
			return r[0]


	def getChatAdmins(self, chat_id: int) -> list[int]:
		self.curs.execute('''SELECT "id" FROM "%s_users" WHERE "admin" = true''', (chat_id,))
		rows = self.curs.fetchall()

		if rows == []:
			return rows
		else:
			for r in rows:
				return[r[0] for r in rows]


	def getChatSettings(self, chat_id: int) -> dict:
		self.curs.execute('''SELECT "chat_defaults" FROM "chats_settings" WHERE "id" = %s''', (chat_id,))
		result = self.curs.fetchall()

		for r in result:
			return r[0]

	def updateChatSettings(self, chat_id: int, settings: str) -> None:
		self.curs.execute('''UPDATE "chats_settings" SET "chat_defaults" = %s WHERE "id" = %s''', (settings, chat_id))


	def getAdminSettings(self, chat_id: int) -> dict:
		self.curs.execute('''SELECT "admin_defaults" FROM "chats_settings" WHERE "id" = %s''', (chat_id,))
		result = self.curs.fetchall()

		for r in result:
			return r[0]

	def updateAdminSettings(self, chat_id: int, settings: str) -> None:
		self.curs.execute('''UPDATE "chats_settings" SET "admin_defaults" = %s WHERE "id" = %s''', (settings, chat_id))

	def close(self):
		self.conn.commit()
		self.conn.close()

pg = DataBase(cfg.databasePath)