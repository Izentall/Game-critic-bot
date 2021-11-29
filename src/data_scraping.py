from bs4 import BeautifulSoup
import requests
from enum import Enum


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

    def get_string_without_date(self):
        return self.score + ", " + self.name + ", " + self.platform

    def get_string(self):
        return self.get_string_without_date() + ", Date: " + self.date


def get_response(url):
    user_agent = {'User-Agent': 'Chrome/94.0.4606.71'}
    response = requests.get(url, headers=user_agent)
    return response


def get_top_5_by_year(year):
    if year < 1916 or year > 2021:
        raise ValueError('Invalid year. Must be between 1916 and 2021. Received year: ' + str(year))
    basic_url = "https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?year_selected=%s&distribution=&sort=desc&view=detailed"
    response = get_response(basic_url % str(year))
    html_soup = BeautifulSoup(response.text, 'html.parser')
    games_container = html_soup.find_all('td', class_='clamp-summary-wrap')[:5]
    result = []
    for i in range(len(games_container)):
        score = games_container[i].a.div.text
        name = games_container[i].find('a', class_='title').h3.text
        platform = games_container[i].find('div', class_='platform').find('span', class_='data').text.strip()
        date = games_container[i].find('div', class_='clamp-details').findAll('span')[2].text
        result.append(Game(score, name, platform, date))
    return result


def get_top_50_for_decade():
    url = "https://www.metacritic.com/feature/best-videogames-of-the-decade-2010s"
    response = get_response(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
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


def get_top_10_by_platform(platform: Platform):
    basic_url = 'https://www.metacritic.com/game/'
    basic_url += platform.value
    response = get_response(basic_url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    games_container = html_soup.find('table', class_='clamp-list')
    games_container = games_container.find_all('td', class_='clamp-summary-wrap')
    result = []
    for i in range(len(games_container)):
        score = games_container[i].a.div.text
        name = games_container[i].h3.text.strip()
        year = games_container[i].find_all('div', class_='clamp-details')[1].span.text
        result.append(Game(score, name, platform.value, year))
    return result


''' Query is a string as it was typed in chat-bot input, with whitespaces, lower/upper cases etc.'''


def get_result_of_query(query: str):
    if query == "":
        raise ValueError("Empty string")
    search_url = "https://www.metacritic.com/search/game/{}/results"
    words = query.split()

    query_word_delimiter = "%20"
    query_url_style = ""
    for word in words:
        query_url_style += word + query_word_delimiter
    query_url_style = query_url_style[:-3]
    search_url = search_url.format(query_url_style)
    response = get_response(search_url)
    html_soup = BeautifulSoup(response.text, 'html.parser')

    if html_soup.find('div', class_='body').p.text.strip() == 'No search results found.':
        raise ValueError("No search results")

    pages_container = html_soup.find('ul', class_='pages')

    games_container = []
    for i in range(len(pages_container)):
        response = get_response(search_url + '?page=' + str(i))
        html_soup = BeautifulSoup(response.text, 'html.parser')
        games_container.append(html_soup.find('ul', class_='search_results module'))

    result = []

    for games in games_container:
        games_container_local = games.find_all('li')
        for game in games_container_local:
            name = game.a.text.strip()
            score = game.span.text.strip()
            platform = game.p.span.text.strip()
            year = game.p.text.split()[2:]

            if len(year) == 1 and year[0] == 'TBA':
                continue

            if len(year) == 2:
                year = year[0] + ' ' + year[1]
            else:
                year = year[0]

            TBA_symbol = game.p.text.split()[-2]
            if TBA_symbol != 'TBA' and year != 'TBA':
                if platform == 'PC':
                    result.append(Game(score, name, 'pc', year))
                if platform == 'XONE':
                    result.append(Game(score, name, 'xbox-one', year))
                if platform == 'PS4':
                    result.append(Game(score, name, 'playstation-4', year))
                if platform == 'PS5':
                    result.append(Game(score, name, 'playstation-5', year))
                if platform == 'Switch':
                    result.append(Game(score, name, 'switch', year))
                if platform == 'XBSX':
                    result.append(Game(score, name, 'xbox-series-x', year))

    if len(result) == 0:
        raise ValueError("No search results")
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
