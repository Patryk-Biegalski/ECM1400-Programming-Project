from covid_data_handler import parse_csv_data , process_covid_csv_data, covid_API_request, update_covid_data
from covid_news_handling import read_config, news_API_request, update_news

def test_parse_csv_data():
    data = parse_csv_data('nation_2021-10-28.csv')
    assert len(data) == 639
def test_process_covid_csv_data ():
    last7days_cases ,current_hospital_cases,total_deaths = process_covid_csv_data(parse_csv_data('nation_2021-10-28.csv'))
    assert last7days_cases == 240299
    assert current_hospital_cases == 7019
    assert total_deaths == 141544

def test_covid_API_request():
    assert type(covid_API_request()) == dict
def test_update_covid_data_local():
    (a,b,c,d) = (update_covid_data())
    assert type(a) == int
    assert type(c) == int
    assert type(d) == str
def test_update_covid_data_national():
    (a,b,c,d) = (update_covid_data('England','nation'))
    assert type(a) == int
    assert type(b) == int
    assert type(c) == int
    assert type(d) == str

def test_read_config():
    assert len(read_config()) == 4
def test_news_API_request():
    assert news_API_request()
def test_update_news():
    assert type(update_news(None,'Covid')) == list

