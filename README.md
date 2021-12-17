![Logotype-with-text](https://user-images.githubusercontent.com/71270225/134701962-4cddf69f-ca4e-404e-87a1-9d19eeed6d39.png)

## Table of contents

* [Introduction](https://github.com/TheTedLab/game-critic-bot#introduction)
* [Contributors](https://github.com/TheTedLab/game-critic-bot#contributors)
* [Docker](https://github.com/TheTedLab/game-critic-bot#docker)

## Introduction

This telegram bot provides viewing of ratings and critic reviews of video games using various contextual filters.

All information is taken from the [www.metacritic.com](https://www.metacritic.com) and parsed by the bot into a chat with the user at his request.

The user can apply various filters to get the top video games for a specific platform, year, all time and other filters, as well as critic reviews for a specific game.

## Contributors

### Группа 3530904/90104

1. Мухин Федор Алексеевич - [TheTedLab](https://github.com/TheTedLab)
2. Хильченко Михаил Юрьевич - [khilchenkomikhail](https://github.com/khilchenkomikhail)
3. Кичигин Юрий Сергеевич - [Izentall](https://github.com/Izentall)
4. Ершов Вадим Дмитриевич - [vadim01er](https://github.com/vadim01er)

## Docker

For building the image with bot and tests  
`docker build -t gamebot .`

To run bot configure the API token and to run test configure the API ID  
```
docker run -e "TOKEN=YOUR-BOT-TOKEN" \
    -e "API_ID=YOUR-API-ID" \
    -e "API_HASH=YOUR-API-HASH" \
    -e "SESSION_STRING=YOUR-SESSION-STRING" \
    -e "BOT_TAG=@YOUR-BOT-TAG" \
    --name gamebot gamebot
```

### Get your `API_ID` and `API_HASH`:
1. Sign in your Telegram account with your phone number [here](https://my.telegram.org/). Then choose “API development tools”
2. If it is your first time doing so, it will ask you for an app name and a short name, you can change both of them later if you need to. Submit the form when you have completed it
3. You will then see the `API_ID` and `API_HASH`

### Get your `SESSION_STRING`:
Run script `get_sessoin_string.py`, located is src/tests, as `python get_sessoin_string.py` and follow instructions