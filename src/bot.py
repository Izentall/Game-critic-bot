import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
)

from authorization import token

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# UTF-8 коды для эмодзи
hand_emoji = u'\U0001F44B'
check_mark = u'\U00002705'
cross_mark = u'\U0000274C'
right_triangle = u'\U000025B6'
memo_emoji = u'\U0001F4DD'
loudspeaker = u'\U0001F4E2'

# Состояния
MENU, TOPS_SUBMENU, TOPS_QUESTION, PLATFORM_SUBMENU, PLATFORM_QUESTION = range(5)
# Переходы
TOPS, PLATFORMS, CURRENT_YEAR, YEAR_2020, DECADE = range(5)
# Платформы
PC, PLAYSTATION, XBOX, SWITCH = range(4)
# Варианты ответа для TOPS
YES_TOPS, NO_TOPS = range(2)
# Варианты ответа для PLATFORMS
YES_PLATFORMS, NO_PLATFORMS = range(2)


def start(update: Update, context: CallbackContext) -> int:
    """Отправить сообщение на `/start`."""
    user = update.message.from_user.full_name
    logger.info("User <%s> started the conversation.", user)
    update.message.reply_text(
        hand_emoji + fr'Привет, {user}!'
    )
    update.message.reply_text(
        'Я информационный бот, который поможет тебе узнать оценки и' +
        ' рецензии на различные видеоигры!' +
        ' Чтобы получить информацию, просто напиши название игры!'
    )
    keyboard = [
        [
            InlineKeyboardButton("Топы Игр", callback_data=str(TOPS)),
            InlineKeyboardButton("Платформы", callback_data=str(PLATFORMS)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Отправка сообщения с текстом и добавлением InlineKeyboard
    update.message.reply_text("Или воспользуйся кнопками:", reply_markup=reply_markup)
    # Переход в состояние MENU
    return MENU


def start_over(update: Update, context: CallbackContext) -> int:
    """Выдает тот же текст и клавиатуру, что и `start`, но не как новое сообщение"""
    # Получить запрос обратного вызова из обновления
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Топы Игр", callback_data=str(TOPS)),
            InlineKeyboardButton("Платформы", callback_data=str(PLATFORMS)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Вместо отправки нового сообщения редактируем сообщение, которое
    # породило запрос обратного вызова.
    query.edit_message_text(text="Или воспользуйся кнопками:", reply_markup=reply_markup)
    # Переход в состояние MENU
    return MENU


def tops(update: Update, context: CallbackContext) -> int:
    """Показать кнопоки топов видеоигр"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("Топ этого года", callback_data=str(CURRENT_YEAR))],
        [InlineKeyboardButton("Топ 2020 года", callback_data=str(YEAR_2020))],
        [InlineKeyboardButton("Топ десятилетия", callback_data=str(DECADE))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Выберите топ видеоигр:", reply_markup=reply_markup
    )
    # Переход в состояние TOPS_SUBMENU
    return TOPS_SUBMENU


def platforms(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора платформы"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("PC", callback_data=str(PC)),
         InlineKeyboardButton("PlayStation", callback_data=str(PLAYSTATION))],
        [InlineKeyboardButton("Xbox", callback_data=str(XBOX)),
         InlineKeyboardButton("Switch", callback_data=str(SWITCH))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Выберите платформу:", reply_markup=reply_markup
    )
    # Переход в состояние PLATFORM_SUBMENU
    return PLATFORM_SUBMENU


def current_year(update: Update, context: CallbackContext) -> int:
    """Информация по топу игр этого года, затем показать новый выбор кнопок"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Да", callback_data=str(YES_TOPS)),
            InlineKeyboardButton("Нет", callback_data=str(NO_TOPS)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Здесь будет запрос данных с метакритики, пока что хардкод
    query.edit_message_text(
        text=
        '1. Disco Elysium: The Final Cut\n' +
        'METASCORE: 97, PLATFORM: PC\n\n' +
        '2. The House in Fata Morgana - Dreams of the Revenants Edition\n' +
        'METASCORE: 97, PLATFORM: SWITCH\n\n' +
        '3. Hades\n' +
        'METASCORE: 93, PLATFORM: XBOX SERIES X\n\n' +
        '4. Hades\n' +
        'METASCORE: 93, PLATFORM: PLAYSTATION 5\n\n' +
        '5. Psychonauts 2\n' +
        'METASCORE: 91, PLATFORM: XBOX\n\n' +
        'Хотите посмотреть другие топы?',
        reply_markup=reply_markup
    )
    # Переход в состояние TOPS_QUESTION
    return TOPS_QUESTION


def year_2020(update: Update, context: CallbackContext) -> int:
    """Информация по топу игр 2020 года, затем показать новый выбор кнопок"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Да", callback_data=str(YES_TOPS)),
            InlineKeyboardButton("Нет", callback_data=str(NO_TOPS)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Здесь будет запрос данных с метакритики, пока что хардкод
    query.edit_message_text(
        text=
        '1. Persona 5 Royal\n' +
        'METASCORE: 95, PLATFORM: PLAYSTATION\n\n' +
        '2. Half-Life: Alyx\n' +
        'METASCORE: 93, PLATFORM: PC\n\n' +
        '3. Hades\n' +
        'METASCORE: 93, PLATFORM: SWITCH\n\n' +
        '4. The Last of Us Part II\n' +
        'METASCORE: 93, PLATFORM: PLAYSTATION 5\n\n' +
        '5. Ori and the Will of the Wisps\n' +
        'METASCORE: 93, PLATFORM: SWITCH\n\n' +
        'Хотите посмотреть другие топы?',
        reply_markup=reply_markup
    )
    # Переход в состояние TOPS_QUESTION
    return TOPS_QUESTION


def decade(update: Update, context: CallbackContext) -> int:
    """Информация по топу игр десятилетия, затем показать новый выбор кнопок"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Да", callback_data=str(YES_TOPS)),
            InlineKeyboardButton("Нет", callback_data=str(NO_TOPS)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Здесь будет запрос данных с метакритики, пока что хардкод
    query.edit_message_text(
        text=
        '1.	Super Mario Galaxy 2\n' +
        'METASCORE: 97, PLATFORM: WII, YEAR: 2010\n\n' +
        '2.	The Legend of Zelda: Breath of the Wild\n' +
        'METASCORE: 97, PLATFORM: SWITCH, YEAR: 2017\n\n' +
        '3.	Red Dead Redemption 2\n' +
        'METASCORE: 97, PLATFORM: PLAYSTATION 4, YEAR: 2018\n\n' +
        '4. Grand Theft Auto V\n' +
        'METASCORE: 97, PLATFORM: PLAYSTATION 4, YEAR: 2014\n\n' +
        '5.	Super Mario Odyssey\n' +
        'METASCORE: 97, PLATFORM: SWITCH, YEAR: 2017\n\n' +
        '6.	Mass Effect 2\n' +
        'METASCORE: 96, PLATFORM: XBOX 360, YEAR: 2010\n\n' +
        '7.	The Elder Scrolls V: Skyrim\n' +
        'METASCORE: 96, PLATFORM: XBOX 360, YEAR: 2011\n\n' +
        '8.	The Last of Us\n' +
        'METASCORE: 95, PLATFORM: PLAYSTATION 3, YEAR: 2013\n\n' +
        '9.	The Last of Us Remastered\n' +
        'METASCORE: 95, PLATFORM: PLAYSTATION 4, YEAR: 2014\n\n' +
        '10. Red Dead Redemption\n' +
        'METASCORE: 95, PLATFORM: XBOX 360, YEAR: 2010\n\n' +
        'Хотите посмотреть другие топы?',
        reply_markup=reply_markup
    )
    # Переход в состояние TOPS_QUESTION
    return TOPS_QUESTION


def end(update: Update, context: CallbackContext) -> int:
    """Возвращает `ConversationHandler.END`, что сообщает устройству
    ConversationHandler, что разговор окончен."""
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Увидимся в следующий раз!")
    return ConversationHandler.END


def pc_func(update: Update, context: CallbackContext) -> int:
    """Информация по топу игр на PC, затем показать новый выбор кнопок"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Да", callback_data=str(YES_PLATFORMS)),
            InlineKeyboardButton("Нет", callback_data=str(NO_PLATFORMS)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Здесь будет запрос данных с метакритики, пока что хардкод
    query.edit_message_text(
        text=
        '1. OPUS: Echo of Starsong\n' +
        'METASCORE: 91\n\n' +
        '2. Psychonauts 2\n' +
        'METASCORE: 89\n\n' +
        '3. Streets of Rage 4: Mr. X Nightmare\n' +
        'METASCORE: 88\n\n' +
        '4. Deathloop\n' +
        'METASCORE: 88\n\n' +
        '5. Townscaper\n' +
        'METASCORE: 86\n\n' +
        'Хотите посмотреть другие платформы?',
        reply_markup=reply_markup
    )
    # Переход в состояние PLATFORM_QUESTION
    return PLATFORM_QUESTION


def playstation_func(update: Update, context: CallbackContext) -> int:
    """Информация по топу игр на Playstation, затем показать новый выбор кнопок"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Да", callback_data=str(YES_PLATFORMS)),
            InlineKeyboardButton("Нет", callback_data=str(NO_PLATFORMS)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Здесь будет запрос данных с метакритики, пока что хардкод
    query.edit_message_text(
        text=
        '1. Hades\n' +
        'METASCORE: 93\n\n' +
        '2. Synth Riders\n' +
        'METASCORE: 89\n\n' +
        '3. Deathloop\n' +
        'METASCORE: 88\n\n' +
        '4. Quake Remastered\n' +
        'METASCORE: 88\n\n' +
        '5. Ghost of Tsushima: Director\'s Cut\n' +
        'METASCORE: 88\n\n' +
        'Хотите посмотреть другие платформы?',
        reply_markup=reply_markup
    )
    # Переход в состояние PLATFORM_QUESTION
    return PLATFORM_QUESTION


def xbox_func(update: Update, context: CallbackContext) -> int:
    """Информация по топу игр на Xbox, затем показать новый выбор кнопок"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Да", callback_data=str(YES_PLATFORMS)),
            InlineKeyboardButton("Нет", callback_data=str(NO_PLATFORMS)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Здесь будет запрос данных с метакритики, пока что хардкод
    query.edit_message_text(
        text=
        '1. Hades\n' +
        'METASCORE: 93\n\n' +
        '2. Psychonauts 2\n' +
        'METASCORE: 91\n\n' +
        '3. Microsoft Flight Simulator\n' +
        'METASCORE: 90\n\n' +
        '4. Streets of Rage 4: Mr. X Nightmare\n' +
        'METASCORE: 89\n\n' +
        '5. Fuga: Melodies of Steel\n' +
        'METASCORE: 89\n\n' +
        'Хотите посмотреть другие платформы?',
        reply_markup=reply_markup
    )
    # Переход в состояние PLATFORM_QUESTION
    return PLATFORM_QUESTION


def switch_func(update: Update, context: CallbackContext) -> int:
    """Информация по топу игр на Switch, затем показать новый выбор кнопок"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Да", callback_data=str(YES_PLATFORMS)),
            InlineKeyboardButton("Нет", callback_data=str(NO_PLATFORMS)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Здесь будет запрос данных с метакритики, пока что хардкод
    query.edit_message_text(
        text=
        '1. A Monster\'s Expedition\n' +
        'METASCORE: 92\n\n' +
        '2. Spelunky 2\n' +
        'METASCORE: 92\n\n' +
        '3. Streets of Rage 4: Mr. X Nightmare\n' +
        'METASCORE: 88\n\n' +
        '4. Metroid Dread\n' +
        'METASCORE: 88\n\n' +
        '5. Quake Remastered\n' +
        'METASCORE: 87\n\n' +
        'Хотите посмотреть другие платформы?',
        reply_markup=reply_markup
    )
    # Переход в состояние PLATFORM_QUESTION
    return PLATFORM_QUESTION


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

        },
        fallbacks=[CommandHandler('start', start)],
    )

    dispatcher.add_handler(conv_handler)

    # Старт бота
    updater.start_polling()

    # Бот работает до прерывания Ctrl-C или получения stop команды
    updater.idle()


if __name__ == '__main__':
    main()
