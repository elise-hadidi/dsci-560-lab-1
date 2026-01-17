import csv
from bs4 import BeautifulSoup

input_file = "../data/raw_data/web_data.html"
market_csv = "../data/processed_data/market_data.csv"
news_csv = "../data/processed_data/news_data.csv"

print("Loading HTML file...")

with open(input_file, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

print("Filtering fields...")

market_data = []
market_cards = soup.find_all("div", class_="MarketCard-marketCard")
for card in market_cards:
    symbol = card.get("data-symbol") or "N/A"
    position = card.get("data-stockposition") or "N/A"
    change = card.get("data-change") or "N/A"
    market_data.append([symbol, position, change])

print("Storing Market data...")

with open(market_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Symbol", "StockPosition", "ChangePct"])
    writer.writerows(market_data)

print(f"Market CSV created: {market_csv}")

news_data = []
latest_news = soup.find_all("div", class_="LatestNews-headlineWrapper")
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
