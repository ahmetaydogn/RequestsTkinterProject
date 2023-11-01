import requests
from bs4 import BeautifulSoup


def get_news_header():
    def get_data_from_web():
        news_url = "https://www.tokathaber.com.tr/son-dakika"
        response = requests.get(news_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    soup = get_data_from_web()

    divs = soup.find_all("div", {"class": "card-body p-3"})
    a_attrs = BeautifulSoup(str(divs), 'html.parser').find_all("a")
    news_title = []
    news_link = []

    for a_attr in a_attrs:
        news_title.append(a_attr.text)
        news_link.append(a_attr['href'])
    return news_title, news_link

def get_weather_and_times_data():
    response = requests.get("http://api.weatherapi.com/v1/forecast.json?key=9aa4bd9900a140ad96d213522233110&q=Tokat&days=7&aqi=no&alerts=no")
    json_array = response.json()
    return json_array

def get_currency_data():
    response = requests.get("http://www.floatrates.com/daily/usd.json")
    currency_json = response.json()
    json_data = currency_json
    return json_data


get_news_header()