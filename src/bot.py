import os

from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler, Filters,
)

from commands import (
    start, start_over, help_func, game_search_func,
    tops, platforms, current_game,
    current_year, year_2020, decade,
    pc_func, playstation_func, xbox_func, switch_func, ps4_func, ps5_func,
    xbox_one_func, xbox_series_func,
    pc_section, switch_section, ps4_section, ps5_section, xbox_one_section,
    xbox_series_section, game_platform_again, end_on_game, game_platform_info, start_fallback,
)
from constants import (
    MENU, TOPS_SUBMENU, TOPS_QUESTION, PLATFORM_SUBMENU, PLATFORM_QUESTION, CURRENT_GAME,
    TOPS, PLATFORMS, CURRENT_YEAR, YEAR_2020, DECADE, ON_GAME, ON_GAME_QUESTION,
    PC, PLAYSTATION, XBOX, SWITCH, CURRENT_GAME_SUBMENU,
    YES_TOPS, NO_TOPS, YES_PLATFORMS, NO_PLATFORMS,
    PLAYSTATION_SUBMENU, PS4, PS5, XBOX_SUBMENU, XBOX_ONE, XBOX_SERIES,
    PC_SECTION, SWITCH_SECTION, PS4_SECTION, PS5_SECTION, XBOX_ONE_SECTION, XBOX_SERIES_SECTION,
    YES_ON_GAME, NO_ON_GAME, ON_SEARCH, SEARCH,
)


def main() -> None:
    """Start the bot."""
    # Создание Updater и связывание с токеном бота
    token = os.getenv('TOKEN')
    updater = Updater(token)

    # Получение dispatcher и регистрация handlers
    dispatcher = updater.dispatcher

    on_game_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(current_game, pattern='^' + str(CURRENT_GAME) + '$')],
        states={
            ON_SEARCH: [
                CallbackQueryHandler(game_platform_info, pattern=Filters.text),
            ],
            ON_GAME: [
                CallbackQueryHandler(pc_section, pattern='^' + str(PC_SECTION) + '$'),
                CallbackQueryHandler(switch_section, pattern='^' + str(SWITCH_SECTION) + '$'),
                CallbackQueryHandler(ps4_section, pattern='^' + str(PS4_SECTION) + '$'),
                CallbackQueryHandler(ps5_section, pattern='^' + str(PS5_SECTION) + '$'),
                CallbackQueryHandler(xbox_one_section, pattern='^' + str(XBOX_ONE_SECTION) + '$'),
                CallbackQueryHandler(xbox_series_section, pattern='^' + str(XBOX_SERIES_SECTION) + '$'),
            ],
            ON_GAME_QUESTION: [
                CallbackQueryHandler(game_platform_again, pattern='^' + str(YES_ON_GAME) + '$'),
            ],
            CURRENT_GAME_SUBMENU: [
                MessageHandler(Filters.text, game_search_func),
            ],
        },
        fallbacks=[
            CallbackQueryHandler(end_on_game, pattern='^' + str(NO_ON_GAME) + '$'),
            CommandHandler('start', start_fallback),
        ],
        map_to_parent={
            NO_ON_GAME: MENU
        },
    )

    action_handlers = [
        CallbackQueryHandler(tops, pattern='^' + str(TOPS) + '$'),
        CallbackQueryHandler(platforms, pattern='^' + str(PLATFORMS) + '$'),
        on_game_conv_handler,
    ]

    # Добавление conversation handler с состояниями разговора
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MENU: action_handlers,
            TOPS_SUBMENU: [
                CallbackQueryHandler(current_year, pattern='^' + str(CURRENT_YEAR) + '$'),
                CallbackQueryHandler(year_2020, pattern='^' + str(YEAR_2020) + '$'),
                CallbackQueryHandler(decade, pattern='^' + str(DECADE) + '$'),
            ],
            TOPS_QUESTION: [
                CallbackQueryHandler(tops, pattern='^' + str(YES_TOPS) + '$'),
                CallbackQueryHandler(start_over, pattern='^' + str(NO_TOPS) + '$'),
            ],
            PLATFORM_SUBMENU: [
                CallbackQueryHandler(pc_func, pattern='^' + str(PC) + '$'),
                CallbackQueryHandler(playstation_func, pattern='^' + str(PLAYSTATION) + '$'),
                CallbackQueryHandler(xbox_func, pattern='^' + str(XBOX) + '$'),
                CallbackQueryHandler(switch_func, pattern='^' + str(SWITCH) + '$'),
            ],
            PLATFORM_QUESTION: [
                CallbackQueryHandler(platforms, pattern='^' + str(YES_PLATFORMS) + '$'),
                CallbackQueryHandler(start_over, pattern='^' + str(NO_PLATFORMS) + '$'),
            ],
            PLAYSTATION_SUBMENU: [
                CallbackQueryHandler(ps4_func, pattern='^' + str(PS4) + '$'),
                CallbackQueryHandler(ps5_func, pattern='^' + str(PS5) + '$'),
            ],
            XBOX_SUBMENU: [
                CallbackQueryHandler(xbox_one_func, pattern='^' + str(XBOX_ONE) + '$'),
                CallbackQueryHandler(xbox_series_func, pattern='^' + str(XBOX_SERIES) + '$'),
            ],
        },
        fallbacks=[
            CommandHandler('start', start),
        ],
    )

    dispatcher.add_handler(conv_handler)

    # Регистрация команд - ответы в Telegram
    dispatcher.add_handler(CommandHandler('help', help_func))

    # Любые сообщения - предположительно название игры
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, game_search_func))

    # Старт бота
    updater.start_polling()

    # Бот работает до прерывания Ctrl-C или получения stop команды
    updater.idle()


if __name__ == '__main__':
    main()
