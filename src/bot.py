from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler, Filters,
)

from authorization import token
from src.commands import (
    start, start_over, new_start, help_func, echo_func,
    tops, platforms,
    current_year, year_2020, decade,
    pc_func, playstation_func, xbox_func, switch_func, ps4_func, ps5_func, xbox_one_func, xbox_series_func,
)
from src.constants import (
    MENU, TOPS_SUBMENU, TOPS_QUESTION, PLATFORM_SUBMENU, PLATFORM_QUESTION,
    TOPS, PLATFORMS, CURRENT_YEAR, YEAR_2020, DECADE, MENU_BACKUP,
    PC, PLAYSTATION, XBOX, SWITCH,
    YES_TOPS, NO_TOPS, YES_PLATFORMS, NO_PLATFORMS, PLAYSTATION_SUBMENU, PS4, PS5, XBOX_SUBMENU, XBOX_ONE, XBOX_SERIES,
)


def main() -> None:
    """Start the bot."""
    # Создание Updater и связывание с токеном бота
    updater = Updater(token)

    # Получение dispatcher и регистрация handlers
    dispatcher = updater.dispatcher

    # Добавление conversation handler с состояниями разговора
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MENU: [
                CallbackQueryHandler(tops, pattern='^' + str(TOPS) + '$'),
                CallbackQueryHandler(platforms, pattern='^' + str(PLATFORMS) + '$'),
            ],
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
            CallbackQueryHandler(new_start, pattern='^' + str(MENU_BACKUP) + '$'),
        ],
    )

    dispatcher.add_handler(conv_handler)

    # Регистрация команд - ответы в Telegram
    dispatcher.add_handler(CommandHandler('help', help_func))

    # Любые сообщения - предположительно название игры
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo_func))

    # Старт бота
    updater.start_polling()

    # Бот работает до прерывания Ctrl-C или получения stop команды
    updater.idle()


if __name__ == '__main__':
    main()
