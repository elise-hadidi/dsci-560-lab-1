import requests
import csv
from bs4 import BeautifulSoup

market_csv = "../data/processed_data/market_data.csv"
news_csv = "../data/processed_data/news_data.csv"
input_file = "../data/raw_data/web_data.html"

url = ("https://quote.cnbc.com/quote-html-webservice/restQuote/symbolType/symbol"
       "?symbols=.STOXX%7C.GDAXI%7C.FTSE%7C.FCHI%7C.FTMIB"
       "&requestMethod=itv&noform=1&partnerId=2&fund=1&exthrs=1&output=json&events=1")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/116.0 Safari/537.36"
}

print("Fetching Market data...")
response = requests.get(url, headers=headers)

if response.status_code != 200:
    print("Failed to fetch market data. Status code:", response.status_code)
    market_data = []
else:
    try:
        data = response.json()
        market_data = []
        for item in data["FormattedQuoteResult"]["FormattedQuote"]:
            symbol = item.get("symbol", "N/A")
            position = item.get("changetype", "N/A")
            change = item.get("change_pct", "N/A")
            market_data.append([symbol, position, change])
        print("Market data fetched successfully.")
    except ValueError:
        print("Market data response is not valid JSON!")
        market_data = []

print("Storing Market data...")
with open(market_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Symbol", "StockPosition", "ChangePct"])
    writer.writerows(market_data)
print(f"Market CSV created: {market_csv}")


print("Loading HTML file for latest news...")
with open(input_file, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

news_data = []
latest_news = soup.find_all("div", class_="LatestNews-headlineWrapper")

print("Filtering Latest News fields...")
for item in latest_news:
    timestamp_tag = item.find("time")
    title_tag = item.find("a")
    timestamp = timestamp_tag.text.strip() if timestamp_tag else "N/A"
    title = title_tag.text.strip() if title_tag else "N/A"
    link = title_tag.get("href") if title_tag else "N/A"
    news_data.append([timestamp, title, link])

print("Storing News data...")
with open(news_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Timestamp", "Title", "Link"])
    writer.writerows(news_data)
print(f"News CSV created: {news_csv}")
