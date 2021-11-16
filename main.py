import requests
import os
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = os.environ.get("STOCK_API_KEY")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")

TWILIO_SID = os.environ.get("TWILIO_SID")
TWILIO_TOKEN = os.environ.get("TWILIO_TOKEN")


# When stock price increase/decreases by 5% between yesterday and the day before yesterday

# Get yesterday's closing stock price
stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}
stock_response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
stock_response.raise_for_status()
stock_data = stock_response.json()["Time Series (Daily)"]
time_series_daily = [value for (key, value) in stock_data.items()]
yesterday_data = time_series_daily[0]
yesterday_closing_price = float(yesterday_data["4. close"])
print(yesterday_closing_price)

# Get day before yesterday's closing stock price
day_before_yesterday_data = time_series_daily[1]
day_before_yesterday_closing_price = float(day_before_yesterday_data["4. close"])
print(day_before_yesterday_closing_price)

# Find the difference between
difference = yesterday_closing_price - day_before_yesterday_closing_price
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"


print(difference)

# Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday
diff_percent = round((difference / yesterday_closing_price) * 100)
print(diff_percent)

# If percentage is greater than 5 then get the first 3 news pieces for the COMPANY_NAME..
if abs(diff_percent) > 1:
    print("Get news")


# use the News API to get articles related to the COMPANY_NAME.
    news_parameters = {
        "qInTitle": STOCK_NAME,
        "apiKey": NEWS_API_KEY
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    news_response.raise_for_status()
    articles = news_response.json()["articles"]


# Create a list that contains the first 3 articles.
    three_articles = articles[:3]


# Create a new list of the first 3 article's headline and description using list comprehension.
    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
    print(formatted_articles)


# Send each article as a separate message via Twilio.
    if yesterday_closing_price >= day_before_yesterday_closing_price:
        icon = "🔺"
    else:
        icon = "🔻"
    for article in formatted_articles:
        client = Client(TWILIO_SID, TWILIO_TOKEN)

        message = client.messages \
            .create(
            body=article,
            from_='+14199633924',
            to='+523317603281'
        )

        print(message.status)




