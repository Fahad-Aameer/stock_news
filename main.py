import requests
from twilio.rest import Client

account_sid = "**********************"
auth_token = "**********************"

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

news_api_key = "0ab95cbaf6bf430981b34241523bb683"
stock_api_key = "SVL3Z1LA6A46UI5M"

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": stock_api_key,
}

news_parameters = {
    "q": COMPANY_NAME,
    "apiKey": news_api_key,
}

stock_response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
stock_response.raise_for_status()
stock_data = stock_response.json()
stock_list = dict(list(stock_data["Time Series (Daily)"].items())[:2])
closing_prices = []

for i in stock_list:
    closing_price = float(stock_list[i]['4. close'])
    closing_prices.append(closing_price)
difference = closing_prices[0] - closing_prices[1]
positive_difference = abs(difference)
percentage = round((positive_difference / closing_prices[1]) * 100)

news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
news_response.raise_for_status()
news_data = news_response.json()

if percentage >= 5:
    news = news_data['articles'][:1]
    headlines = news[0]['title']
    brief = news[0]['description']
    client = Client(account_sid, auth_token)
    if difference > 0:
        message = client.messages \
            .create(
            body=f"TSLA: 🔺{percentage}%\nHeadlines: {headlines}\nBrief: {brief}",
            from_='+19704998758',
            to='**********'
        )
        print(message.status)
    else:
        message = client.messages \
            .create(
            body=f"TSLA: 🔻{percentage}%\nHeadlines: {headlines}\nBrief: {brief}",
            from_='+19704998758',
            to='**********'
        )
        print(message.status)
