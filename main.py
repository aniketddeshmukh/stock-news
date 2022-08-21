import requests
import creds #file containing all API keys
from datetime import date,timedelta
from twilio.rest import Client

STOCK_NAME = "ADANIGREEN.BSE"
COMPANY_NAME = "Adani Green Energy"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"

today = date.today() - timedelta(days=1)
yesterday= today-timedelta(days=2)

news_url =f"https://newsapi.org/v2/everything?q={COMPANY_NAME}&from={today}&to={yesterday}&sortBy=popularity&apiKey={creds.NEWS_API_KEY}"
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK_NAME}&outputsize=full&apikey={creds.API_KEY}'

r= requests.get(url)
data =r.json()

Today_Close= float(list(data["Time Series (Daily)"].values())[0]["4. close"])
Yest_Close =float(list(data["Time Series (Daily)"].values())[1]["4. close"])
news=[]

diff = abs(Today_Close-Yest_Close)/Yest_Close
Diff =round(diff,3)
print(Today_Close)
print(Yest_Close)
print(f"{Diff} %")

if diff>=0:
    r2 =requests.get(news_url)
    r2.raise_for_status()
    print(r2.json())
    data2 =r2.json()['articles']
    news = data2[:3]

if (Today_Close-Yest_Close)/Yest_Close >0:
    symbol= "🔺"
else:
    symbol="🔻"
print(f"{STOCK_NAME}:{symbol}{Diff} %")

formatted_articles = [f"{STOCK_NAME}: {symbol}{Diff}% \nHeadline: {article['title']}. \nBrief: {article['description']}" for article in news]
print(formatted_articles)


client = Client(creds.account_sid, creds.auth_token)
for article in formatted_articles:
    print(article)
for article in formatted_articles:
    message = client.messages.create(
                                  body=article,
                                  from_=creds.from_no,
                                  to=creds.to_no
                              )

    # print(message.sid)
