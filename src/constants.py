from telegram import InlineKeyboardButton

# UTF-8 коды для эмодзи
hand_emoji = u'\U0001F44B'
check_mark = u'\U00002705'
cross_mark = u'\U0000274C'
right_triangle = u'\U000025B6'
memo_emoji = u'\U0001F4DD'
loudspeaker = u'\U0001F4E2'

# Состояния
MENU, TOPS_SUBMENU, TOPS_QUESTION, PLATFORM_SUBMENU, PLAYSTATION_SUBMENU, \
    XBOX_SUBMENU, PLATFORM_QUESTION = range(7)
# Переходы
TOPS, PLATFORMS, CURRENT_YEAR, YEAR_2020, DECADE, MENU_BACKUP, \
    PS4, PS5, XBOX_ONE, XBOX_SERIES = range(10)
# Платформы
PC, PLAYSTATION, XBOX, SWITCH = range(4)
# Варианты ответа для TOPS
YES_TOPS, NO_TOPS = range(2)
# Варианты ответа для PLATFORMS
YES_PLATFORMS, NO_PLATFORMS = range(2)

# Константные тексты
greetings_text = "Я информационный бот, который поможет тебе узнать оценки\n" \
                 "и рецензии на различные видеоигры!\n" \
                 "Чтобы получить информацию, просто напиши название игры!"

using_buttons_text = "Или воспользуйся кнопками:"
select_top_text = "Выберите топ видеоигр:"
select_platform_text = "Выберите платформу:"
want_see_tops_text = "Хотите посмотреть другие топы?"
want_see_platforms_text = "Хотите посмотреть другие платформы?"
help_text = "/start - начать разговор\n" \
            "/help - помощь\n" \
            "Чтобы получить информацию, просто напиши название игры\n" \
            "или воспользуйся кнопками меню!"

# Клавиатуры кнопок
keyboard_MENU = [
    [
        InlineKeyboardButton("Топы Игр", callback_data=str(TOPS)),
        InlineKeyboardButton("Платформы", callback_data=str(PLATFORMS)),
    ]
]

keyboard_TOPS = [
    [InlineKeyboardButton("Топ этого года", callback_data=str(CURRENT_YEAR))],
    [InlineKeyboardButton("Топ 2020 года", callback_data=str(YEAR_2020))],
    [InlineKeyboardButton("Топ десятилетия", callback_data=str(DECADE))],
]

keyboard_PLATFORMS = [
    [InlineKeyboardButton("PC", callback_data=str(PC)),
     InlineKeyboardButton("PlayStation", callback_data=str(PLAYSTATION))],
    [InlineKeyboardButton("Xbox", callback_data=str(XBOX)),
     InlineKeyboardButton("Switch", callback_data=str(SWITCH))],
]

keyboard_PLAYSTATION_SUBMENU = [
    [InlineKeyboardButton("PS4", callback_data=str(PS4))],
    [InlineKeyboardButton("PS5", callback_data=str(PS5))],
]

keyboard_XBOX_SUBMENU = [
    [InlineKeyboardButton("Xbox One", callback_data=str(XBOX_ONE))],
    [InlineKeyboardButton("Xbox Series X", callback_data=str(XBOX_SERIES))],
]

keyboard_QUESTION_TOPS = [
    [
        InlineKeyboardButton("Да", callback_data=str(YES_TOPS)),
        InlineKeyboardButton("Нет", callback_data=str(NO_TOPS)),
    ]
]

keyboard_QUESTION_PLATFORMS = [
    [
        InlineKeyboardButton("Да", callback_data=str(YES_PLATFORMS)),
        InlineKeyboardButton("Нет", callback_data=str(NO_PLATFORMS)),
    ]
]

keyboard_ON_GAME = [
    [
        InlineKeyboardButton("Назад в меню", callback_data=str(MENU_BACKUP))
    ]
]
