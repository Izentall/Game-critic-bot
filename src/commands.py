import logging

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
import data_scraping
import datetime

from src.constants import (
    hand_emoji,
    MENU, TOPS_SUBMENU, TOPS_QUESTION, PLATFORM_SUBMENU, PLATFORM_QUESTION,
    PLAYSTATION_SUBMENU, XBOX_SUBMENU,
    greetings_text, using_buttons_text, select_top_text, select_platform_text,
    want_see_tops_text, want_see_platforms_text, help_text,
    keyboard_MENU, keyboard_TOPS, keyboard_PLATFORMS, keyboard_QUESTION_TOPS,
    keyboard_QUESTION_PLATFORMS, keyboard_ON_GAME, keyboard_PLAYSTATION_SUBMENU, keyboard_XBOX_SUBMENU,
    PC_SECTION, SWITCH_SECTION, PS4_SECTION, PS5_SECTION, XBOX_ONE_SECTION, XBOX_SERIES_SECTION,
    ON_GAME, ON_GAME_QUESTION, CURRENT_GAME_SUBMENU, CURRENT_DATA, NO_ON_GAME,
    keyboard_ON_GAME_QUESTION
)

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> int:
    """Отправить сообщение на `/start`."""
    user = update.message.from_user.full_name
    logger.info("User <%s> started the conversation.", user)
    update.message.reply_text(
        hand_emoji + fr'Привет, {user}!'
    )
    update.message.reply_text(greetings_text)
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_MENU)
    # Отправка сообщения с текстом и добавлением InlineKeyboard
    update.message.reply_text(using_buttons_text, reply_markup=reply_markup_keyboard)
    # Переход в состояние MENU
    return MENU


def start_over(update: Update, context: CallbackContext) -> int:
    """Выдает тот же текст и клавиатуру, что и `start`, но не как новое сообщение"""
    # Получить запрос обратного вызова из обновления
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_MENU)
    # Вместо отправки нового сообщения редактируем сообщение, которое
    # породило запрос обратного вызова.
    query.edit_message_text(text=using_buttons_text, reply_markup=reply_markup_keyboard)
    # Переход в состояние MENU
    return MENU


def tops(update: Update, context: CallbackContext) -> int:
    """Показать кнопоки топов видеоигр"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_TOPS)
    query.edit_message_text(text=select_top_text, reply_markup=reply_markup_keyboard)
    # Переход в состояние TOPS_SUBMENU
    return TOPS_SUBMENU


def platforms(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора платформы"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_PLATFORMS)
    query.edit_message_text(text=select_platform_text, reply_markup=reply_markup_keyboard)
    # Переход в состояние PLATFORM_SUBMENU
    return PLATFORM_SUBMENU


def current_game(update: Update, context: CallbackContext) -> int:
    """Показать информацию о поиске конкретной игры"""
    query = update.callback_query
    # Сохраняем ввод названия игры
    context.user_data[CURRENT_DATA] = query.data
    query.answer()
    query.edit_message_text(text='Напишите название интересующей вас игры!')
    # Переход в состояние CURRENT_GAME_SUBMENU
    return CURRENT_GAME_SUBMENU


def current_year(update: Update, context: CallbackContext) -> int:
    """Информация по топу игр этого года, затем показать новый выбор кнопок"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_QUESTION_TOPS)

    out_text = data_scraping.get_top_string(year=datetime.datetime.now().year)
    query.edit_message_text(
        text=out_text + want_see_tops_text,
        reply_markup=reply_markup_keyboard
    )
    # Переход в состояние TOPS_QUESTION
    return TOPS_QUESTION


def year_2020(update: Update, context: CallbackContext) -> int:
    """Информация по топу игр 2020 года, затем показать новый выбор кнопок"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_QUESTION_TOPS)

    out_text = data_scraping.get_top_string(year=datetime.datetime.now().year - 1)
    query.edit_message_text(
        text=out_text + want_see_tops_text,
        reply_markup=reply_markup_keyboard
    )
    # Переход в состояние TOPS_QUESTION
    return TOPS_QUESTION


def decade(update: Update, context: CallbackContext) -> int:
    """Информация по топу игр десятилетия, затем показать новый выбор кнопок"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_QUESTION_TOPS)
    out_text = data_scraping.get_top_string()
    query.edit_message_text(
        text=out_text + want_see_tops_text,
        reply_markup=reply_markup_keyboard
    )
    # Переход в состояние TOPS_QUESTION
    return TOPS_QUESTION


def pc_func(update: Update, context: CallbackContext) -> int:
    """Информация по топу игр на PC, затем показать новый выбор кнопок"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_QUESTION_PLATFORMS)
    out_text = data_scraping.get_top_platform_string(data_scraping.Platform.PC)
    query.edit_message_text(
        text='TOP PC Games:\n' + out_text + want_see_platforms_text,
        reply_markup=reply_markup_keyboard
    )
    # Переход в состояние PLATFORM_QUESTION
    return PLATFORM_QUESTION


def playstation_func(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора Playstation"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_PLAYSTATION_SUBMENU)
    query.edit_message_text(text=select_platform_text, reply_markup=reply_markup_keyboard)
    # Переход в состояние PLAYSTATION_SUBMENU
    return PLAYSTATION_SUBMENU


def ps4_func(update: Update, context: CallbackContext) -> int:
    """Информация по топу игр на Playstation 4, затем показать новый выбор кнопок"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_QUESTION_PLATFORMS)
    out_text = data_scraping.get_top_platform_string(data_scraping.Platform.PS4)
    query.edit_message_text(
        text='TOP PlayStation 4 Games:\n' + out_text + want_see_platforms_text,
        reply_markup=reply_markup_keyboard
    )
    # Переход в состояние PLATFORM_QUESTION
    return PLATFORM_QUESTION


def ps5_func(update: Update, context: CallbackContext) -> int:
    """Информация по топу игр на Playstation 5, затем показать новый выбор кнопок"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_QUESTION_PLATFORMS)
    out_text = data_scraping.get_top_platform_string(data_scraping.Platform.PS5)
    query.edit_message_text(
        text='TOP PlayStation 5 Games:\n' + out_text + want_see_platforms_text,
        reply_markup=reply_markup_keyboard
    )
    # Переход в состояние PLATFORM_QUESTION
    return PLATFORM_QUESTION


def xbox_func(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора Xbox"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_XBOX_SUBMENU)
    query.edit_message_text(text=select_platform_text, reply_markup=reply_markup_keyboard)
    # Переход в состояние XBOX_SUBMENU
    return XBOX_SUBMENU


def xbox_one_func(update: Update, context: CallbackContext) -> int:
    """Информация по топу игр на Xbox One, затем показать новый выбор кнопок"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_QUESTION_PLATFORMS)
    out_text = data_scraping.get_top_platform_string(data_scraping.Platform.XboxOne)
    query.edit_message_text(
        text='TOP XboxOne Games:\n' + out_text + want_see_platforms_text,
        reply_markup=reply_markup_keyboard
    )
    # Переход в состояние PLATFORM_QUESTION
    return PLATFORM_QUESTION


def xbox_series_func(update: Update, context: CallbackContext) -> int:
    """Информация по топу игр на Xbox Series X, затем показать новый выбор кнопок"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_QUESTION_PLATFORMS)
    out_text = data_scraping.get_top_platform_string(data_scraping.Platform.XboxSeries)
    query.edit_message_text(
        text='TOP XboxSeries X Games:\n' + out_text + want_see_platforms_text,
        reply_markup=reply_markup_keyboard
    )
    # Переход в состояние PLATFORM_QUESTION
    return PLATFORM_QUESTION


def switch_func(update: Update, context: CallbackContext) -> int:
    """Информация по топу игр на Switch, затем показать новый выбор кнопок"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_QUESTION_PLATFORMS)
    out_text = data_scraping.get_top_platform_string(data_scraping.Platform.Switch)
    query.edit_message_text(
        text='TOP Switch Games:\n' + out_text + want_see_platforms_text,
        reply_markup=reply_markup_keyboard
    )
    # Переход в состояние PLATFORM_QUESTION
    return PLATFORM_QUESTION


def help_func(update: Update, context: CallbackContext):
    """Возвращает информацию о всех командах и функциях"""
    update.message.reply_text(text=help_text)


def game_info_func(update: Update, context: CallbackContext) -> int:
    """Возвращает информацию по конкретной игре"""
    user_data = context.user_data
    # if (update.message.text == Filters.command):
    #   update.message.reply_text('No commands in name!')
    user_data[CURRENT_DATA] = update.message.text
    game_name = user_data[CURRENT_DATA]
    # Тут будет вызов функции поиска игры на сайте, пока что хардкод
    # if (game_name.search())
    # else reply_text('Игра не найдена в поиске\n')
    # Тут будет вызов функции поиска платформ игры, если она есть в поиске
    # game_platforms = game_name.get_platforms_names()
    game_platforms = ['PC', 'PS4', 'PS5', 'XboxOne', 'XboxSeries']
    inline_keyboard_platform_buttons(game_platforms)
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_ON_GAME)
    update.message.reply_text(game_name, reply_markup=reply_markup_keyboard)
    # Переход в состояние ON_GAME
    return ON_GAME


def game_info_again(update: Update, context: CallbackContext) -> int:
    """Возвращает информацию по конкретной игре при повторном вызове"""
    user_data = context.user_data
    query = update.callback_query
    query.answer()
    game_name = user_data[CURRENT_DATA]
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_ON_GAME)
    query.edit_message_text(text=game_name, reply_markup=reply_markup_keyboard)
    # Переход в состояние ON_GAME
    return ON_GAME


def get_platform_button(platform_button: str):
    """Возвращает ID кнопки по строке"""
    if platform_button == "PC":
        return PC_SECTION
    elif platform_button == "Switch":
        return SWITCH_SECTION
    elif platform_button == "PS4":
        return PS4_SECTION
    elif platform_button == "PS5":
        return PS5_SECTION
    elif platform_button == "XboxOne":
        return XBOX_ONE_SECTION
    elif platform_button == "XboxSeries":
        return XBOX_SERIES_SECTION


def inline_keyboard_platform_buttons(game_platforms: []):
    # Очистка клавиатуры
    keyboard_ON_GAME.clear()
    for platform_button in game_platforms:
        keyboard_ON_GAME.insert(
            0,
            [InlineKeyboardButton(
                platform_button, callback_data=str(get_platform_button(platform_button))
            )]
        )


def pc_section(update: Update, context: CallbackContext):
    """Возвращает информацию по конкретной игре на PC"""
    query = update.callback_query
    query.answer()
    game_name = context.user_data[CURRENT_DATA] + ' - PC\n'
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_ON_GAME_QUESTION)
    # Тут будет запрос информации об игре с PC платформы, пока что хардкод
    out_text = 'Metascore: 86 - based on 92 Critic Reviews\n' + \
               'User Score: 7.1 - based on 30182 Ratings\n' + \
               'Developer: CD Projekt Red Studio' + \
               'Genre(s): Action RPG, Role-Playing, Action RPG\n' + \
               '# of players: No Online Multiplayer\n' + \
               'Rating: M\n'
    # out_text = data_scraping.get_game_info_from_pc()
    query.edit_message_text(
        text=game_name + out_text + want_see_platforms_text,
        reply_markup=reply_markup_keyboard
    )
    # Переход в состояние ON_GAME_QUESTION
    return ON_GAME_QUESTION


def switch_section(update: Update, context: CallbackContext):
    """Возвращает информацию по конкретной игре на Switch"""
    query = update.callback_query
    query.answer()
    game_name = context.user_data[CURRENT_DATA] + ' - Switch\n'
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_ON_GAME_QUESTION)
    # Тут будет запрос информации об игре с PC платформы, пока что хардкод
    out_text = 'Metascore: 80 - based on 32 Critic Reviews\n' + \
               'User Score: 6.9 - based on 20178 Ratings\n' + \
               'Developer: CD Projekt Red Studio' + \
               'Genre(s): Action RPG, Role-Playing, Action RPG\n' + \
               '# of players: No Online Multiplayer\n' + \
               'Rating: M\n'
    # out_text = data_scraping.get_game_info_from_pc()
    query.edit_message_text(
        text=game_name + out_text + want_see_platforms_text,
        reply_markup=reply_markup_keyboard
    )
    # Переход в состояние ON_GAME_QUESTION
    return ON_GAME_QUESTION


def ps4_section(update: Update, context: CallbackContext):
    """Возвращает информацию по конкретной игре на PlayStation 4"""
    query = update.callback_query
    query.answer()
    game_name = context.user_data[CURRENT_DATA] + ' - PS4\n'
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_ON_GAME_QUESTION)
    # Тут будет запрос информации об игре с PC платформы, пока что хардкод
    out_text = 'Metascore: 57 - based on 38 Critic Reviews\n' + \
               'User Score: 3.7 - based on 10201 Ratings\n' + \
               'Developer: CD Projekt Red Studio' + \
               'Genre(s): Action RPG, Role-Playing, Action RPG\n' + \
               '# of players: No Online Multiplayer\n' + \
               'Rating: M\n'
    # out_text = data_scraping.get_game_info_from_pc()
    query.edit_message_text(
        text=game_name + out_text + want_see_platforms_text,
        reply_markup=reply_markup_keyboard
    )
    # Переход в состояние ON_GAME_QUESTION
    return ON_GAME_QUESTION


def ps5_section(update: Update, context: CallbackContext):
    """Возвращает информацию по конкретной игре на PlayStation 5"""
    query = update.callback_query
    query.answer()
    game_name = context.user_data[CURRENT_DATA] + ' - PS5\n'
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_ON_GAME_QUESTION)
    # Тут будет запрос информации об игре с PC платформы, пока что хардкод
    out_text = 'Metascore: 85 - based on 65 Critic Reviews\n' + \
               'User Score: 5.7 - based on 45143 Ratings\n' + \
               'Developer: CD Projekt Red Studio' + \
               'Genre(s): Action RPG, Role-Playing, Action RPG\n' + \
               '# of players: No Online Multiplayer\n' + \
               'Rating: M\n'
    # out_text = data_scraping.get_game_info_from_pc()
    query.edit_message_text(
        text=game_name + out_text + want_see_platforms_text,
        reply_markup=reply_markup_keyboard
    )
    # Переход в состояние ON_GAME_QUESTION
    return ON_GAME_QUESTION


def xbox_one_section(update: Update, context: CallbackContext):
    """Возвращает информацию по конкретной игре на XboxOne"""
    query = update.callback_query
    query.answer()
    game_name = context.user_data[CURRENT_DATA] + ' - XboxOne\n'
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_ON_GAME_QUESTION)
    # Тут будет запрос информации об игре с PC платформы, пока что хардкод
    out_text = 'Metascore: 61 - based on 16 Critic Reviews\n' + \
               'User Score: 4.9 - based on 4079 Ratings\n' + \
               'Developer: CD Projekt Red Studio' + \
               'Genre(s): Action RPG, Role-Playing, Action RPG\n' + \
               '# of players: No Online Multiplayer\n' + \
               'Rating: M\n'
    # out_text = data_scraping.get_game_info_from_pc()
    query.edit_message_text(
        text=game_name + out_text + want_see_platforms_text,
        reply_markup=reply_markup_keyboard
    )
    # Переход в состояние ON_GAME_QUESTION
    return ON_GAME_QUESTION


def xbox_series_section(update: Update, context: CallbackContext):
    """Возвращает информацию по конкретной игре на XboxSeries X"""
    query = update.callback_query
    query.answer()
    game_name = context.user_data[CURRENT_DATA] + ' - XboxSeries X\n'
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_ON_GAME_QUESTION)
    # Тут будет запрос информации об игре с PC платформы, пока что хардкод
    out_text = 'Metascore: 71 - based on 49 Critic Reviews\n' + \
               'User Score: 8.9 - based on 6589 Ratings\n' + \
               'Developer: CD Projekt Red Studio' + \
               'Genre(s): Action RPG, Role-Playing, Action RPG\n' + \
               '# of players: No Online Multiplayer\n' + \
               'Rating: M\n'
    # out_text = data_scraping.get_game_info_from_pc()
    query.edit_message_text(
        text=game_name + out_text + want_see_platforms_text,
        reply_markup=reply_markup_keyboard
    )
    # Переход в состояние ON_GAME_QUESTION
    return ON_GAME_QUESTION


def end_on_game(update: Update, context: CallbackContext) -> int:
    """End on game conversation and return to main conversation."""
    new_start(update, context)
    return NO_ON_GAME


def new_start(update: Update, context: CallbackContext):
    """Возвращает текст и клавиатуру к главному меню"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_MENU)
    query.edit_message_text(text=using_buttons_text, reply_markup=reply_markup_keyboard)
    # Переход в состояние MENU
    return MENU
