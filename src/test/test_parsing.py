import pytest
from pathlib import Path
from src.data_scraping import get_top_5_by_year, get_top_50_for_decade, get_top_10_by_platform, Platform
from src.test.test_constatns import TOP_5_OF_2021, TOP_5_OF_2020, TOP_10_OF_DECADE, TOP_10_BY_PLATFORM


@pytest.mark.parsing
@pytest.mark.parametrize(
    'year, filename, result',
    [
        pytest.param(2021, 'top_5_of_2021.html', TOP_5_OF_2021),
        pytest.param(2020, 'top_5_of_2020.html', TOP_5_OF_2020)
    ]
)
def test_get_top_5_by_year(year, filename, result):
    file = open(Path(Path.cwd(), 'src', 'test', 'html_pages', filename), 'r', encoding='utf-8')
    top___by_year = get_top_5_by_year(year, text=file.read())
    out_text = ''
    for game in top___by_year[:5]:
        out_text += game.get_string_without_date() + "\n"
    assert out_text[:-1] == result


@pytest.mark.parsing
def test_get_top_50_for_decade():
    file = open(Path(Path.cwd(), 'src', 'test', 'html_pages', 'top_10_of_decade.html'), 'r', encoding='utf-8')
    top___by_year_decade = get_top_50_for_decade(text=file.read())
    out_text = ''
    for game in top___by_year_decade[:10]:
        out_text += game.get_string_without_date() + "\n"
    assert out_text[:-1] == TOP_10_OF_DECADE


@pytest.mark.parsing
def test_get_top_10_by_platform():
    file = open(Path(Path.cwd(), 'src', 'test', 'html_pages', 'top_10_by_platform.html'), 'r', encoding='utf-8')
    top_by_platform = get_top_10_by_platform(Platform('pc'), text=file.read())
    out_text = ''
    for game in top_by_platform[:10]:
        out_text += game.get_string_without_platform() + "\n"
    assert out_text[:-1] == TOP_10_BY_PLATFORM
