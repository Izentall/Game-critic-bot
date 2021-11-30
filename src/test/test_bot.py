import datetime
import time

import pytest
from pytest import mark
from telethon import TelegramClient
from telethon.tl.custom.message import Message
from telethon.tl.custom.conversation import Conversation

from src import data_scraping
from src.constants import (greetings_text, using_buttons_text, select_top_text, keyboard_MENU, keyboard_TOPS,
                           keyboard_QUESTION_TOPS, select_platform_text, keyboard_PLATFORMS,
                           keyboard_QUESTION_PLATFORMS, want_see_tops_text, keyboard_PLAYSTATION_SUBMENU,
                           keyboard_XBOX_SUBMENU)

@pytest.mark.bot
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
        await check_keyboard(resp, keyboard_MENU, using_buttons_text)


@pytest.mark.bot
@pytest.mark.parametrize(
    'button_index, year',
    [
        pytest.param(0, datetime.datetime.now().year),
        pytest.param(1, datetime.datetime.now().year - 1),
        pytest.param(2, None)
    ]
)
@mark.asyncio
async def test_tops(client: TelegramClient, button_index: int, year):
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
        await check_keyboard(resp, keyboard_TOPS, select_top_text)
        await resp.click(text=keyboard_TOPS[button_index][0].text)

        # Bot < Хотите посмотреть другие топы?
        # [Да] [Нет]
        resp = await get_last_message(client, conv, timeout=1)
        await check_certain_top(resp, year)
        await resp.click(text=keyboard_QUESTION_TOPS[0][0].text)

        # Bot < Выберите топ видеоигр:
        # [Топ этого года]
        # [Топ 2020 года]
        # [Топ десятилетия]
        resp = await get_last_message(client, conv)
        await check_keyboard(resp, keyboard_TOPS, select_top_text)
        await resp.click(text=keyboard_TOPS[button_index][0].text)

        # Bot < Хотите посмотреть другие топы?
        # [Да] [Нет]
        resp = await get_last_message(client, conv, timeout=1)
        await check_certain_top(resp, year)
        await resp.click(text=keyboard_QUESTION_TOPS[0][1].text)

        # Bot < Или воспользуйся кнопками:
        # [Топы Игр][Платформы]
        resp = await get_last_message(client, conv)
        await check_keyboard(resp, keyboard_MENU, using_buttons_text)


@pytest.mark.bot
@pytest.mark.parametrize(
    'button_index, submenu',
    [
        pytest.param((0, 0), None),
        pytest.param((0, 1), keyboard_PLAYSTATION_SUBMENU),
        pytest.param((1, 0), keyboard_XBOX_SUBMENU),
        pytest.param((1, 1), None)
    ]
)
@mark.asyncio
async def test_platforms(client: TelegramClient, button_index: tuple, submenu: list):
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

        amount = get_keyboard_length(submenu) if submenu is not None else 1
        for i in range(amount):
            await resp.click(text=keyboard_MENU[0][1].text)

            # Bot < Выберите платформу:
            # [PC] [PS]
            # [Xbox] [Switch]
            resp = await get_last_message(client, conv)
            await check_keyboard(resp, keyboard_PLATFORMS, select_platform_text)
            await resp.click(text=keyboard_PLATFORMS[button_index[0]][button_index[1]].text)

            if submenu is not None:
                # Bot < Выберите платформу:
                # [первая кнопка]
                # [вторая кнопка]
                resp = await get_last_message(client, conv)
                await check_keyboard(resp, submenu, select_platform_text)
                await resp.click(text=submenu[i][0].text)

            # Bot < Хотите посмотреть другие платформы?
            # [Да] [Нет]
            resp = await get_last_message(client, conv)
            await check_certain_platform(resp)
            await resp.click(text=keyboard_QUESTION_PLATFORMS[0][0].text)

            # Bot < Выберите платформу:
            # [PC] [PS]
            # [Xbox] [Switch]
            resp = await get_last_message(client, conv)
            await check_keyboard(resp, keyboard_PLATFORMS, select_platform_text)
            await resp.click(text=keyboard_PLATFORMS[button_index[0]][button_index[1]].text)

            if submenu is not None:
                # Bot < Выберите платформу:
                # [первая кнопка]
                # [вторая кнопка]
                resp = await get_last_message(client, conv)
                await check_keyboard(resp, submenu, select_platform_text)
                await resp.click(text=submenu[i][0].text)

            # Bot < Хотите посмотреть другие платформы?
            # [Да] [Нет]
            resp = await get_last_message(client, conv)
            await check_certain_platform(resp)
            await resp.click(text=keyboard_QUESTION_PLATFORMS[0][1].text)

            # Bot < Или воспользуйся кнопками:
            # [Топы Игр][Платформы]
            resp = await get_last_message(client, conv)
            await check_keyboard(resp, keyboard_MENU, using_buttons_text)


async def check_certain_top(resp: Message, year):
    assert data_scraping.get_top_string(year=year) in resp.raw_text
    assert want_see_tops_text in resp.raw_text
    assert resp.button_count == get_keyboard_length(keyboard_QUESTION_TOPS)
    for i in range(len(resp.buttons)):
        for j in range(len(resp.buttons[i])):
            assert resp.buttons[i][j].text == keyboard_QUESTION_TOPS[i][j].text


async def check_certain_platform(resp: Message):
    # Пока захардкодил, так как не увидел парсинга инфы с сайта в боте
    assert "1. " in resp.raw_text
    assert "2. " in resp.raw_text
    assert "3. " in resp.raw_text
    assert "4. " in resp.raw_text
    assert "5. " in resp.raw_text
    assert resp.button_count == get_keyboard_length(keyboard_QUESTION_PLATFORMS)
    for i in range(len(resp.buttons)):
        for j in range(len(resp.buttons[i])):
            assert resp.buttons[i][j].text == keyboard_QUESTION_PLATFORMS[i][j].text


async def check_keyboard(resp: Message, keyboard, message_text):
    assert message_text in resp.raw_text
    len_keyboard = get_keyboard_length(keyboard)
    assert resp.button_count == len_keyboard
    for i in range(len(resp.buttons)):
        for j in range(len(resp.buttons[i])):
            assert resp.buttons[i][j].text == keyboard[i][j].text


async def get_last_message(client: TelegramClient, conv: Conversation, timeout=0.15):
    time.sleep(timeout)
    messages_list = await client.get_messages(conv.chat)
    return messages_list[0]


def get_keyboard_length(keyboard):
    len_keyboard = 0
    for elem in keyboard:
        len_keyboard += len(elem)
    return len_keyboard
