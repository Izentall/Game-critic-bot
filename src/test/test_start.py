from pytest import mark
from secrets import token_urlsafe
from telethon import TelegramClient
from telethon.tl.custom.message import Message
from telethon.tl.types.messages import BotCallbackAnswer


@mark.asyncio
async def test_start(client: TelegramClient):
    # Create a conversation
    with client.conversation("@GameMetaCriticBot", timeout=5) as conv:
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
        assert "Я информационный бот" in resp.raw_text
        assert "Чтобы получить информацию" in resp.raw_text

        # Bot < Или воспользуйся кнопками:
        # [Топы Игр][Платформы]
        resp = await conv.get_response()
        assert "Или воспользуйся кнопками" in resp.raw_text
        assert resp.button_count == 2
        assert resp.buttons[0][0].text == "Топы Игр"
        assert resp.buttons[0][1].text == "Платформы"
