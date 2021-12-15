import ast
import datetime
import logging

import telegram
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

import data_scraping
from constants import (
    hand_emoji,
    MENU, TOPS_SUBMENU, TOPS_QUESTION, PLATFORM_SUBMENU, PLATFORM_QUESTION,
    PLAYSTATION_SUBMENU, XBOX_SUBMENU,
    greetings_text, using_buttons_text, select_top_text, select_platform_text,
    want_see_tops_text, want_see_platforms_text, help_text, game_search_list,
    keyboard_MENU, keyboard_TOPS, keyboard_PLATFORMS, keyboard_QUESTION_TOPS,
    keyboard_QUESTION_PLATFORMS, keyboard_ON_SEARCH, keyboard_PLAYSTATION_SUBMENU, keyboard_XBOX_SUBMENU,
    PC_SECTION, SWITCH_SECTION, PS4_SECTION, PS5_SECTION, XBOX_ONE_SECTION, XBOX_SERIES_SECTION,
    ON_GAME, ON_GAME_QUESTION, CURRENT_GAME_SUBMENU, CURRENT_DATA, NO_ON_GAME,
    keyboard_ON_GAME_QUESTION, keyboard_ONLY_BACK, ON_SEARCH, keyboard_ON_GAME,
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

    with open('images/metacritic_logo.png', 'rb') as photo:
        update.message.reply_photo(
            photo=photo,
            caption=using_buttons_text,
            reply_markup=reply_markup_keyboard
        )

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

    with open('images/metacritic_logo.png', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=using_buttons_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние MENU
    return MENU


def tops(update: Update, context: CallbackContext) -> int:
    """Показать кнопоки топов видеоигр"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_TOPS)

    with open('images/metacritic_logo.png', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_top_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние TOPS_SUBMENU
    return TOPS_SUBMENU


def platforms(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора платформы"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_PLATFORMS)

    with open('images/metacritic_logo.png', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_platform_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние PLATFORM_SUBMENU
    return PLATFORM_SUBMENU


def current_game(update: Update, context: CallbackContext) -> int:
    """Показать информацию о поиске конкретной игры"""
    query = update.callback_query
    # Сохраняем ввод названия игры
    context.user_data[CURRENT_DATA] = query.data
    query.answer()

    with open('images/metacritic_logo.png', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption='Напишите название интересующей вас игры!',
    )

    # Переход в состояние CURRENT_GAME_SUBMENU
    return CURRENT_GAME_SUBMENU


def current_year(update: Update, context: CallbackContext) -> int:
    """Информация по топу игр этого года, затем показать новый выбор кнопок"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_QUESTION_TOPS)

    out_text = data_scraping.get_top_string(year=datetime.datetime.now().year)

    with open('images/metacritic_logo.png', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=out_text + want_see_tops_text,
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

    with open('images/metacritic_logo.png', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=out_text + want_see_tops_text,
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

    with open('images/metacritic_logo.png', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=out_text + want_see_tops_text,
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

    with open('images/metacritic_logo.png', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption='TOP PC Games:\n' + out_text + want_see_platforms_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние PLATFORM_QUESTION
    return PLATFORM_QUESTION


def playstation_func(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора Playstation"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_PLAYSTATION_SUBMENU)

    with open('images/metacritic_logo.png', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_platform_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние PLAYSTATION_SUBMENU
    return PLAYSTATION_SUBMENU


def ps4_func(update: Update, context: CallbackContext) -> int:
    """Информация по топу игр на Playstation 4, затем показать новый выбор кнопок"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_QUESTION_PLATFORMS)
    out_text = data_scraping.get_top_platform_string(data_scraping.Platform.PS4)

    with open('images/metacritic_logo.png', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption='TOP PlayStation 4 Games:\n' + out_text + want_see_platforms_text,
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

    with open('images/metacritic_logo.png', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption='TOP PlayStation 5 Games:\n' + out_text + want_see_platforms_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние PLATFORM_QUESTION
    return PLATFORM_QUESTION


def xbox_func(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора Xbox"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_XBOX_SUBMENU)

    with open('images/metacritic_logo.png', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_platform_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние XBOX_SUBMENU
    return XBOX_SUBMENU


def xbox_one_func(update: Update, context: CallbackContext) -> int:
    """Информация по топу игр на Xbox One, затем показать новый выбор кнопок"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_QUESTION_PLATFORMS)
    out_text = data_scraping.get_top_platform_string(data_scraping.Platform.XboxOne)

    with open('images/metacritic_logo.png', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption='TOP XboxOne Games:\n' + out_text + want_see_platforms_text,
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

    with open('images/metacritic_logo.png', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption='TOP XboxSeries X Games:\n' + out_text + want_see_platforms_text,
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

    with open('images/metacritic_logo.png', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption='TOP Switch Games:\n' + out_text + want_see_platforms_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние PLATFORM_QUESTION
    return PLATFORM_QUESTION


def help_func(update: Update, context: CallbackContext):
    """Возвращает информацию о всех командах и функциях"""
    update.message.reply_text(text=help_text)


def game_search_func(update: Update, context: CallbackContext) -> int:
    """Возвращает информацию поиска по конкретной игре"""
    user_data = context.user_data
    # if (update.message.text == Filters.command):
    #   update.message.reply_text('No commands in name!')
    user_data[CURRENT_DATA] = update.message.text
    game_name = user_data[CURRENT_DATA]
    game_search_list.clear()
    game_search_list.extend(data_scraping.get_result_of_query(game_name))

    if len(game_search_list) != 0:
        game_search_list.reverse()
        inline_keyboard_game_search_buttons(game_search_list)
        reply_markup_keyboard = InlineKeyboardMarkup(keyboard_ON_SEARCH)
        with open('images/search.png', 'rb') as photo:
            update.message.reply_photo(
                photo=photo,
                caption="Результаты поиска для " + game_name + ": ",
                reply_markup=reply_markup_keyboard
            )
        # Переход в состояние ON_SEARCH
        return ON_SEARCH
    else:
        with open('images/no_search_results.png', 'rb') as photo:
            update.message.reply_photo(
                photo=photo,
                caption="Нет результатов поиска",
                reply_markup=InlineKeyboardMarkup(keyboard_ONLY_BACK)
            )
        # Переход в состояние ON_GAME_QUESTION -> выход в меню
        return ON_GAME_QUESTION


def game_platform_info(update: Update, context: CallbackContext) -> int:
    """Возвращает информацию по платформам выбранной игры"""
    user_data = context.user_data
    call = update.callback_query
    if call.data.startswith("['game'"):
        game_index = ast.literal_eval(call.data)[1]
        buttons = InlineKeyboardMarkup(keyboard_ON_SEARCH).to_dict()
        buttons_list = buttons["inline_keyboard"]
        buttons_list.reverse()
        game_to_platform = buttons["inline_keyboard"][int(game_index)][0]["text"]
        user_data[CURRENT_DATA] = game_to_platform
        inline_keyboard_game_platform_buttons(game_to_platform, game_search_list)
        reply_markup_keyboard = InlineKeyboardMarkup(keyboard_ON_GAME)

        with open('images/search.png', 'rb') as photo:
            image = telegram.InputMediaPhoto(photo)

        call.edit_message_media(
            media=image
        )

        call.edit_message_caption(
            caption="Платформы для " + game_to_platform + ": ",
            reply_markup=reply_markup_keyboard
        )

    # Переход в состояние ON_GAME
    return ON_GAME


def game_platform_again(update: Update, context: CallbackContext) -> int:
    """Возвращает информацию по платформам конкретной игры при повторном вызове"""
    user_data = context.user_data
    query = update.callback_query
    query.answer()
    game_name = user_data[CURRENT_DATA]
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_ON_GAME)

    with open('images/search.png', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption="Платформы для " + game_name + ": ",
        reply_markup=reply_markup_keyboard
    )
    # Переход в состояние ON_GAME
    return ON_GAME


def get_platform_button(platform: str):
    """Возвращает ID кнопки по строке"""
    if platform == "pc":
        return PC_SECTION
    elif platform == "switch":
        return SWITCH_SECTION
    elif platform == "playstation-4":
        return PS4_SECTION
    elif platform == "playstation-5":
        return PS5_SECTION
    elif platform == "xbox-one":
        return XBOX_ONE_SECTION
    elif platform == "xbox-series-x":
        return XBOX_SERIES_SECTION


def inline_keyboard_game_search_buttons(game_search: []):
    # Получаем только уникальные игры из поиска
    unique_games = list({game.name: game for game in game_search}.values())
    # Очистка клавиатуры
    keyboard_ON_SEARCH.clear()
    for game in unique_games:
        keyboard_ON_SEARCH.insert(
            0,
            [InlineKeyboardButton(
                game.name, callback_data="['game', '" + str(unique_games.index(game)) + "']"
            )]
        )


def get_platform_name(platform: str):
    """Возвращает название платформы по строке"""
    if platform == "pc":
        return "PC"
    elif platform == "switch":
        return "Switch"
    elif platform == "playstation-4":
        return "PlayStation 4"
    elif platform == "playstation-5":
        return "PlayStation 5"
    elif platform == "xbox-one":
        return "Xbox One"
    elif platform == "xbox-series-x":
        return "Xbox Series X"


def inline_keyboard_game_platform_buttons(searched_game: str, game_search: []):
    # Очистка клавиатуры
    keyboard_ON_GAME.clear()
    game_search.sort(key=lambda x: x.platform, reverse=True)
    for game in game_search:
        if game.name == searched_game:
            keyboard_ON_GAME.insert(
                0,
                [InlineKeyboardButton(
                    get_platform_name(game.platform),
                    callback_data=get_platform_button(game.platform)
                )]
            )


def pc_section(update: Update, context: CallbackContext):
    """Возвращает информацию по конкретной игре на PC"""
    query = update.callback_query
    query.answer()
    game_name = context.user_data[CURRENT_DATA]
    game_title = game_name + ' - PC\n'
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_ON_GAME_QUESTION)
    out_text = ''
    for game in game_search_list:
        if game.platform == 'pc' and game.name == game_name:
            out_text = get_out_text_for_platform(game)
            data_scraping.get_game_image(game)

    with open('images/game_image.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo.read())

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=game_title + out_text + want_see_platforms_text,
        reply_markup=reply_markup_keyboard
    )
    # Переход в состояние ON_GAME_QUESTION
    return ON_GAME_QUESTION


def switch_section(update: Update, context: CallbackContext):
    """Возвращает информацию по конкретной игре на Switch"""
    query = update.callback_query
    query.answer()
    game_name = context.user_data[CURRENT_DATA]
    game_title = game_name + ' - Switch\n'
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_ON_GAME_QUESTION)
    out_text = ''
    for game in game_search_list:
        if game.platform == 'switch' and game.name == game_name:
            out_text = get_out_text_for_platform(game)
            data_scraping.get_game_image(game)

    with open('images/game_image.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo.read())

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=game_title + out_text + want_see_platforms_text,
        reply_markup=reply_markup_keyboard
    )
    return ON_GAME_QUESTION


def ps4_section(update: Update, context: CallbackContext):
    """Возвращает информацию по конкретной игре на PlayStation 4"""
    query = update.callback_query
    query.answer()
    game_name = context.user_data[CURRENT_DATA]
    game_title = game_name + ' - PS4\n'
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_ON_GAME_QUESTION)
    out_text = ''
    for game in game_search_list:
        if game.platform == 'playstation-4' and game.name == game_name:
            out_text = get_out_text_for_platform(game)
            data_scraping.get_game_image(game)

    with open('images/game_image.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo.read())

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=game_title + out_text + want_see_platforms_text,
        reply_markup=reply_markup_keyboard
    )
    return ON_GAME_QUESTION


def ps5_section(update: Update, context: CallbackContext):
    """Возвращает информацию по конкретной игре на PlayStation 5"""
    query = update.callback_query
    query.answer()
    game_name = context.user_data[CURRENT_DATA]
    game_title = game_name + ' - PS5\n'
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_ON_GAME_QUESTION)
    out_text = ''
    for game in game_search_list:
        if game.platform == 'playstation-5' and game.name == game_name:
            out_text = get_out_text_for_platform(game)
            data_scraping.get_game_image(game)

    with open('images/game_image.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo.read())

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=game_title + out_text + want_see_platforms_text,
        reply_markup=reply_markup_keyboard
    )
    return ON_GAME_QUESTION


def xbox_one_section(update: Update, context: CallbackContext):
    """Возвращает информацию по конкретной игре на XboxOne"""
    query = update.callback_query
    query.answer()
    game_name = context.user_data[CURRENT_DATA]
    game_title = game_name + ' - XboxOne\n'
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_ON_GAME_QUESTION)
    out_text = ''
    for game in game_search_list:
        if game.platform == 'xbox-one' and game.name == game_name:
            out_text = get_out_text_for_platform(game)
            data_scraping.get_game_image(game)

    with open('images/game_image.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo.read())

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=game_title + out_text + want_see_platforms_text,
        reply_markup=reply_markup_keyboard
    )
    return ON_GAME_QUESTION


def xbox_series_section(update: Update, context: CallbackContext):
    """Возвращает информацию по конкретной игре на XboxSeries X"""
    query = update.callback_query
    query.answer()
    game_name = context.user_data[CURRENT_DATA]
    game_title = game_name + ' - XboxSeries X\n'
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_ON_GAME_QUESTION)
    out_text = ''
    for game in game_search_list:
        if game.platform == 'xbox-series-x' and game.name == game_name:
            out_text = get_out_text_for_platform(game)
            data_scraping.get_game_image(game)

    with open('images/game_image.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo.read())

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=game_title + out_text + want_see_platforms_text,
        reply_markup=reply_markup_keyboard
    )
    return ON_GAME_QUESTION


def get_out_text_for_platform(game) -> str:
    game_data = data_scraping.get_description_score_details_by_game(game)
    return 'Release Date: ' + game.date + '\n' + \
           'Metascore: ' + game.score + ' - based on ' + game_data[3] + ' Critic Reviews\n' + \
           'User Score: ' + game_data[1] + ' - based on ' + game_data[2] + ' Ratings\n' + \
           game_data[0] + '\n'


def end_on_game(update: Update, context: CallbackContext) -> int:
    """End on game conversation and return to main conversation."""
    new_start(update, context)
    return NO_ON_GAME


def start_fallback(update, context) -> int:
    start(update, context)
    return NO_ON_GAME


def new_start(update: Update, context: CallbackContext):
    """Возвращает текст и клавиатуру к главному меню"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_MENU)

    with open('images/metacritic_logo.png', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=using_buttons_text,
        reply_markup=reply_markup_keyboard
    )
    # Переход в состояние MENU
    return MENU
