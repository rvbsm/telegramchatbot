import psycopg2
import config as cfg

class DataBase:
	def __init__(self, path):
		self.conn = psycopg2.connect(path)
		self.curs = self.conn.cursor()
		self.conn.autocommit = True

	def createTables(self, user_id: int, chat_id: int, chat_title: str, counter: int):
		self.curs.execute('''CREATE TABLE IF NOT EXISTS "%s_users" (
			"id" serial PRIMARY KEY NOT NULL,
			"name" text,
			"admin" bool DEFAULT false,
			"warn" smallint DEFAULT 0,
			"msg_counter" integer DEFAULT 0
		)''', (chat_id,))
		self.curs.execute('''INSERT INTO "%s_users"("id", "admin") VALUES(%s, %s) ON CONFLICT ("id") DO UPDATE SET "admin" = true''', (chat_id, user_id, True))

		self.curs.execute('''CREATE TABLE IF NOT EXISTS "commands" (
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
			"lang" text DEFAULT 'ru_RU'
		)''')
		self.curs.execute('''INSERT INTO "chats_settings"("id", "title", "msg_counter") VALUES(%s, %s, %s) ON CONFLICT ("id") DO NOTHING''', (chat_id, chat_title, counter))


	def getUsers(self, chat_id: int):
		self.curs.execute('''SELECT "id" FROM "%s_users"''', (chat_id,))
		rows = self.curs.fetchall()
		for r in rows:
			return[r[0] for r in rows]

	def existUser(self, user_id: int, chat_id: int):
		self.curs.execute('''SELECT * FROM "%s_users" WHERE "id" = %s''', (chat_id, user_id))
		result = self.curs.fetchall()
		return bool(len(result))

	def addUser(self, user_id: int, chat_id: int, username: str):
		self.curs.execute('''INSERT INTO "%s_users"("id", "name") VALUES(%s, %s) ON CONFLICT ("id") DO NOTHING''', (chat_id, user_id, username))

	def setUserName(self, user_id: int, chat_id: int, username: str):
		self.curs.execute('''UPDATE "%s_users" SET "name" = %s WHERE "id" = %s''', (chat_id, username, user_id))


	def getUserStatus(self, user_id: int, chat_id: int):
		self.curs.execute('''SELECT "admin" FROM "%s_users" WHERE "id" = %s''', (chat_id, user_id))
		result = self.curs.fetchall()
		for r in result:
			return r[0]

	def setUserStatus(self, user_id: int, chat_id: int, status: bool):
		self.curs.execute('''UPDATE "%s_users" SET "admin" = %s WHERE "id" = %s''', (chat_id, status, user_id))


	def getUserCounter(self, user_id: int, chat_id: int):
		self.curs.execute('''SELECT "msg_counter" FROM "%s_users" WHERE "id" = %s''', (chat_id, user_id))
		result = self.curs.fetchall()
		for r in result:
			return r[0]

	def updateUserCounter(self, user_id: int, chat_id: int):
		counter = self.getUserCounter(user_id, chat_id) + 1
		self.curs.execute('''UPDATE "%s_users" SET "msg_counter" = %s WHERE "id" = %s''', (chat_id, counter, user_id))


	def getUserWarn(self, user_id: int, chat_id: int):
		self.curs.execute('''SELECT "warn" FROM "%s_users" WHERE "id" = %s''', (chat_id, user_id))
		result = self.curs.fetchall()
		for r in result:
			return r[0]

	def addUserWarn(self, user_id: int, chat_id: int):
		warn = self.getUserWarn(user_id, chat_id) + 1
		self.curs.execute('''UPDATE "%s_users" SET "warn" = %s WHERE "id" = %s''', (chat_id, warn, user_id))

	def removeUserWarn(self, user_id: int, chat_id: int):
		self.curs.execute('''UPDATE "%s_users" SET "warn" = 0 WHERE "id" = %s''', (chat_id, user_id))


	def getCommandsList(self, chat_id: int):
		self.curs.execute('''SELECT "command" FROM "commands" WHERE "id" = %s''', (chat_id,))
		rows = self.curs.fetchall()
		
		if rows == []:
			return rows
		else:
			for r in rows:
				return[r[0] for r in rows]

	def getCommandOutput(self, chat_id: int, command: str):
		self.curs.execute('''SELECT "output" FROM "commands" WHERE "command" = %s AND "id" = %s''', (command, chat_id))
		result = self.curs.fetchall()
		for r in result:
			return r[0]

	def addCommand(self, chat_id: int, command: str, output: str):
		self.curs.execute('''INSERT INTO "commands"("id", "command", "output") VALUES(%s, %s, %s)''', (chat_id, command, output))

	def editCommand(self, chat_id: int, command: str, output: str):
		self.curs.execute('''UPDATE "commands" SET "output" = %s WHERE "id" = %s AND "command" = %s''', (output, chat_id, command))

	def removeCommand(self, chat_id: int, command: str):
		self.curs.execute('''DELETE FROM "commands" WHERE "id" = %s AND "command" = %s''', (chat_id, command))


	def getChatLang(self, chat_id: int):
		self.curs.execute('''SELECT "lang" FROM "chats_settings" WHERE "id" = %s''', (chat_id,))
		result = self.curs.fetchall()
		for r in result:
			return r[0]

	def setChatLang(self, chat_id: int, lang: str):
		self.curs.execute('''UPDATE "chats_settings" SET "lang" = %s WHERE "id" = %s''', (lang, chat_id))


	def getChatMaxWarns(self, chat_id: int):
		self.curs.execute('''SELECT "max_warns" FROM "chats_settings" WHERE "id" = %s''', (chat_id,))
		result = self.curs.fetchall()
		for r in result:
			return r[0]


	def getChatAdmins(self, chat_id: int):
		self.curs.execute('''SELECT "id" FROM "%s_users" WHERE "admin" = true''', (chat_id,))
		rows = self.curs.fetchall()

		if rows == []:
			return rows
		else:
			for r in rows:
				return[r[0] for r in rows]


	def close(self):
		self.conn.commit()
		self.conn.close()

pg = DataBase(cfg.databasePath)