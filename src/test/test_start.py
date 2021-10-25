from pytest import mark
from secrets import token_urlsafe
from telethon import TelegramClient
from telethon.tl.custom.message import Message
from telethon.tl.types.messages import BotCallbackAnswer
from src.constants import (keyboard_MENU, greetings_text, using_buttons_text)


@mark.asyncio
async def test_start(client: TelegramClient):
    # Create a conversation
    async with client.conversation("@GameMetaCriticTestBot", timeout=5) as conv:
        # User > /start
        await conv.send_message("/start")
        # Bot < Привет, {user}!

        # Get response
        resp: Message = await conv.get_response()
        # Make assertions
        assert "Привет" in resp.raw_text

        # Bot < Я информационный бот, который поможет тебе узнать оценки рецензии на различные видеоигры!
        # Чтобы получить информацию, просто напиши название игры!
        resp = await conv.get_response()
        assert greetings_text in resp.raw_text

        # Bot < Или воспользуйся кнопками:
        # [Топы Игр][Платформы]
        resp = await conv.get_response()
        assert using_buttons_text in resp.raw_text
        assert resp.button_count == len(keyboard_MENU[0])
        assert resp.buttons[0][0].text == keyboard_MENU[0][0].text
        assert resp.buttons[0][1].text == keyboard_MENU[0][1].text
