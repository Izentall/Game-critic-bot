import pytest
from telethon import TelegramClient
from telethon.sessions import StringSession
from api_data import api_id, api_hash, session_str


@pytest.fixture(scope="session")
async def client() -> TelegramClient:
    # Connect to the server
    await client.connect()
    # Issue a high level command to start receiving message
    await client.get_me()
    # Fill the entity cache
    await client.get_dialogs()

    yield TelegramClient(
        StringSession(session_str), api_id, api_hash,
        sequential_updates=True
    )

    await client.disconnect()
    await client.disconnected
