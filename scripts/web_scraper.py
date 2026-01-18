import requests
from bs4 import BeautifulSoup

url = "https://www.cnbc.com/world/?region=world"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

print("Status code:", response.status_code)

if response.status_code != 200:
    print("Failed to retrieve page")
    exit()

html_content = response.text

with open("../data/raw_data/web_data.html", "w", encoding="utf-8") as f:
    f.write(html_content)

