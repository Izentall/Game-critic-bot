from enum import Enum

import requests
from bs4 import BeautifulSoup


class Platform(Enum):
    PC = 'pc'
    Switch = 'switch'
    PS4 = 'playstation-4'
    PS5 = 'playstation-5'
    XboxOne = 'xbox-one'
    XboxSeries = 'xbox-series-x'


class Game(object):
    def __init__(self, score, name, platform, date):
        self.score = score
        self.name = name
        self.platform = platform
        self.date = date

    def __str__(self):
        return self.name + ' ' + self.platform + ' ' + self.date + ' ' + self.score

    def get_string_without_platform(self):
        return self.score + ", " + self.name

    def get_string_without_date(self):
        return self.get_string_without_platform() + ", " + self.platform

    def get_string(self):
        return self.get_string_without_date() + ", Date: " + self.date


def get_response(url):
    user_agent = {'User-Agent': 'Chrome/94.0.4606.71'}
    response = requests.get(url, headers=user_agent)
    return response


def get_top_5_by_year(year, text=None):
    if text is None:
        if year < 1916 or year > 2021:
            raise ValueError('Invalid year. Must be between 1916 and 2021. Received year: ' + str(year))
        basic_url = "https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?year_selected=%s&distribution=&sort=desc&view=detailed"
        text = get_response(basic_url % str(year)).text
    html_soup = BeautifulSoup(text, 'html.parser')
    games_container = html_soup.find_all('td', class_='clamp-summary-wrap')[:5]
    result = []
    for i in range(len(games_container)):
        score = games_container[i].a.div.text
        name = games_container[i].find('a', class_='title').h3.text
        platform = games_container[i].find('div', class_='platform').find('span', class_='data').text.strip()
        date = games_container[i].find('div', class_='clamp-details').findAll('span')[2].text
        result.append(Game(score, name, platform, date))
    return result


def get_top_50_for_decade(text=None):
    if text is None:
        url = "https://www.metacritic.com/feature/best-videogames-of-the-decade-2010s"
        text = get_response(url).text
    html_soup = BeautifulSoup(text, 'html.parser')
    games_container = html_soup.find('table', class_='bordertable')
    games_container = games_container.table.tbody.find_all('tr')
    result = []
    for i in range(len(games_container)):
        game_number = games_container[i].td.text
        game = games_container[i].text
        year = game[game.rfind(',') + 1:game.rfind(')')].strip()
        score = game[game.rfind(')') + 1:]
        platform = game[game.rfind('(') + 1:game.rfind(',')]
        game = game.replace(game_number, "")
        name = game[:game.rfind('(')].strip()
        result.append(Game(score, name, platform, year))
    return result


def get_top_10_by_platform(platform: Platform, text=None):
    if text is None:
        basic_url = 'https://www.metacritic.com/game/'
        basic_url += platform.value
        text = get_response(basic_url).text
    html_soup = BeautifulSoup(text, 'html.parser')
    games_container = html_soup.find('table', class_='clamp-list')
    games_container = games_container.find_all('td', class_='clamp-summary-wrap')
    result = []
    for i in range(len(games_container)):
        score = games_container[i].a.div.text
        name = games_container[i].h3.text.strip()
        year = games_container[i].find_all('div', class_='clamp-details')[1].span.text
        result.append(Game(score, name, platform.value, year))
    return result


def get_top_string(year=None):
    if year is not None:
        top___by_year = get_top_5_by_year(year)
        out_text = ''
        for game in top___by_year[:5]:
            out_text += game.get_string_without_date() + "\n"
    else:
        top___by_year_decade = get_top_50_for_decade()
        out_text = ''
        for game in top___by_year_decade[:10]:
            out_text += game.get_string_without_date() + "\n"
    return out_text


def get_top_platform_string(platform: Platform):
    top_by_platform = get_top_10_by_platform(platform)
    out_text = ''
    for game in top_by_platform[:10]:
        out_text += game.get_string_without_platform() + "\n"
    return out_text
