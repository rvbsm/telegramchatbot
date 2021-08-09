import os

botToken = os.getenv("botToken")
botName = os.getenv("botName")

databaseUrl = os.getenv("DATABASE_URL")
databasePath = f"""
user={databaseUrl.split('/')[2].split('@')[0].split(':')[0]} 
password={databaseUrl.split('/')[2].split('@')[0].split(':')[1]} 
host={databaseUrl.split('/')[2].split('@')[1].split(':')[0]} 
port={databaseUrl.split('/')[2].split('@')[1].split(':')[1]} 
dbname={databaseUrl.split('/')[3]}"""

webhookPath = "/webhook/" + botToken
webhookUrl = f"https://{botName}.herokuapp.com" + webhookPath
