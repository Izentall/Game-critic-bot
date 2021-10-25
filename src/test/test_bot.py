import time

import pytest
from pytest import mark
from telethon import TelegramClient
from telethon.tl.custom.message import Message
from telethon.tl.custom.conversation import Conversation
from src.constants import (greetings_text, using_buttons_text, select_top_text, keyboard_MENU, keyboard_TOPS,
                           keyboard_QUESTION_TOPS)


@mark.asyncio
async def test_start(client: TelegramClient):
    # Create a conversation
    async with client.conversation("@GameMetaCriticTestBot", timeout=5) as conv:
        # User > /start
        await conv.send_message("/start")

        # Get response
        # Bot < Привет, {user}!
        resp: Message = await conv.get_response()
        assert "Привет" in resp.raw_text

        # Bot < Я информационный бот, который поможет тебе узнать оценки рецензии на различные видеоигры!
        # Чтобы получить информацию, просто напиши название игры!
        resp = await conv.get_response()
        assert greetings_text in resp.raw_text

        resp = await conv.get_response()
        await check_main_menu(resp)


@pytest.mark.parametrize(
    'button_index',
    [
        pytest.param(0),
        pytest.param(1),
        pytest.param(2)
    ]
)
@mark.asyncio
async def test_tops(client: TelegramClient, button_index):
    # Create a conversation
    async with client.conversation("@GameMetaCriticTestBot", timeout=5) as conv:
        # User > /start
        await conv.send_message("/start")

        # Get response
        # Bot < Привет, {user}!
        resp: Message = await conv.get_response()

        # Bot < Я информационный бот, который поможет тебе узнать оценки рецензии на различные видеоигры!
        # Чтобы получить информацию, просто напиши название игры!
        resp = await conv.get_response()

        # Bot < Или воспользуйся кнопками:
        # [Топы Игр][Платформы]
        resp = await conv.get_response()
        await resp.click(text=keyboard_MENU[0][0].text)

        # Bot < Выберите топ видеоигр:
        # [Топ этого года]
        # [Топ 2020 года]
        # [Топ десятилетия]
        resp = await get_last_message(client, conv)
        await check_top_keyboard(resp)
        await resp.click(text=keyboard_TOPS[button_index][0].text)

        # Bot < Хотите посмотреть другие топы?
        # [Да] [Нет]
        resp = await get_last_message(client, conv)
        await check_certain_top(resp)
        await resp.click(text=keyboard_QUESTION_TOPS[0][0].text)

        # Bot < Выберите топ видеоигр:
        # [Топ этого года]
        # [Топ 2020 года]
        # [Топ десятилетия]
        resp = await get_last_message(client, conv)
        await check_top_keyboard(resp)
        await resp.click(text=keyboard_TOPS[button_index][0].text)

        # Bot < Хотите посмотреть другие топы?
        # [Да] [Нет]
        resp = await get_last_message(client, conv)
        await check_certain_top(resp)
        await resp.click(text=keyboard_QUESTION_TOPS[0][1].text)

        # Bot < Или воспользуйся кнопками:
        # [Топы Игр][Платформы]
        resp = await get_last_message(client, conv)
        await check_main_menu(resp)


async def check_main_menu(resp: Message):
    # Bot < Или воспользуйся кнопками:
    # [Топы Игр][Платформы]
    assert using_buttons_text in resp.raw_text
    assert resp.button_count == len(keyboard_MENU[0])
    for i in range(resp.button_count):
        assert resp.buttons[0][i].text == keyboard_MENU[0][i].text


async def check_top_keyboard(resp: Message):
    assert select_top_text in resp.raw_text
    assert resp.button_count == len(keyboard_TOPS)
    for i in range(resp.button_count):
        assert resp.buttons[i][0].text == keyboard_TOPS[i][0].text


async def check_certain_top(resp: Message):
    # Пока захардкодил, так как не увидел парсинга инфы с сайта в боте
    assert "1. " in resp.raw_text
    assert "2. " in resp.raw_text
    assert "3. " in resp.raw_text
    assert "4. " in resp.raw_text
    assert "5. " in resp.raw_text
    assert resp.button_count == len(keyboard_QUESTION_TOPS[0])
    for i in range(resp.button_count):
        assert resp.buttons[0][i].text == keyboard_QUESTION_TOPS[0][i].text


async def get_last_message(client: TelegramClient, conv: Conversation):
    time.sleep(0.1)
    messages_list = await client.get_messages(conv.chat)
    return messages_list[0]
