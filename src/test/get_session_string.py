from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from api_data import api_id, api_hash


with TelegramClient(StringSession(), api_id, api_hash) as client:
    print("Your session string is:", client.session.save())
