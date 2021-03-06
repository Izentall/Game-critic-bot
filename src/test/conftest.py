import asyncio
import os

import pytest
from telethon import TelegramClient
from telethon.sessions import StringSession


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope="session")
async def client() -> TelegramClient:
    api_id = os.getenv('API_ID')
    api_hash = os.getenv('API_HASH')
    session_str = os.getenv('SESSION_STRING')
    telegram_client: TelegramClient = TelegramClient(
        StringSession(session_str), api_id, api_hash,
        sequential_updates=True
    )
    # Connect to the server
    await telegram_client.connect()
    # Issue a high level command to start receiving message
    await telegram_client.get_me()
    # Fill the entity cache
    await telegram_client.get_dialogs()

    yield telegram_client

    await telegram_client.disconnect()
    await telegram_client.disconnected
