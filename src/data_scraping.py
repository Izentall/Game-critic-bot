from bs4 import BeautifulSoup
import requests


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
        result.append((score, name, platform, date))
    return result


def get_top_50_for_decade():
    url = "https://www.metacritic.com/feature/best-videogames-of-the-decade-2010s"
    responce = get_response(url)
    html_soup = BeautifulSoup(responce.text, 'html.parser')
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
        result.append((score, name, platform, year))
    return result

# def main():
#     for game in get_top_5_by_year(2021):
#         string = ""
#         for attribute in game:
#             string += attribute + " "
#         print(string)
#
#     for game in get_top_5_by_year(2020):
#         string = ""
#         for attribute in game:
#             string += attribute + " "
#         print(string)
#     for game in get_top_50_by_decade():
#         string = ""
#         for attribute in game:
#             string += attribute + " "
#         print(string)
#
# if __name__ == "__main__":
#     main()
