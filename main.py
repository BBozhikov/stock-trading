import requests
import datetime

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
API_KEY = "9KO8AZRQ6S7PP61P"


def get_news():
    params_for_news = {
        "q": COMPANY_NAME,
        "from": datetime.datetime.now().strftime("%Y:%m:%d"),
        "sortBy": "popularity",
        "apiKey": "edf2b5639ee444849d55d74b238c2145",

    }

    response = requests.get("https://newsapi.org/v2/everything", params=params_for_news)
    response.raise_for_status()

    news = response.json()["articles"]

    news = news[0:3]

    for i in range(len(news) - 1):
        headline = news[i]["title"]
        brief = news[i]["description"]
        print(f"Headline: {headline}\nBrief: {brief}")


params = {
    "function":  "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": API_KEY,

}

respond = requests.get("https://www.alphavantage.co/query", params=params)
respond.raise_for_status()
# print(respond.status_code)

data = respond.json()

time_now = datetime.datetime.now()

day = time_now.day
month = time_now.month
year = time_now.year

day -= 1
if day < 10:
    day = f"0{day}"
if month < 10:
    month = f"0{month}"
date_to_fill = f"{year}-{month}-{day}"
try:
    yesterday_data = data["Time Series (Daily)"][date_to_fill]
    day = int(day)
    day -= 1

    if day < 10:
        day = f"0{day}"

    date_to_fill = f"{year}-{month}-{day}"
    the_day_before_data = data["Time Series (Daily)"][date_to_fill]
except KeyError:
    print(f"no data for {date_to_fill}")
else:
    perc = float(the_day_before_data["4. close"]) - float(yesterday_data["1. open"])
    perc = perc / float(yesterday_data["1. open"]) * 100
    if perc > 0:
        print(f"Tesla prices rose by {round(perc)}%🔺")

        get_news()
    else:
        print(f"Tesla prices has fallen by {round(perc)}%🔻")
        get_news()


