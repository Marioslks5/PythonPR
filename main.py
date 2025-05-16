import requests
from bs4 import BeautifulSoup

url = "https://www.coinlore.com/"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# List for storing cryptocurrencies
cryptos = []

rows = soup.find_all("tr", attrs={"data-id": True})

for row in rows[:10]:
    crypto_name = row.find("td", class_="currency-name")
    crypto_price_div = row.find("div", class_="table-price-class")
    change_24h = row.find("div", class_="h24_change")
    change_7d = row.find("div", class_="7d_change2")
    total_volume = row.find("td", class_="market-cap")
    h24_volume = row.find("div", class_="table-volume-class")

    if crypto_name and crypto_price:
        name = crypto_name.find("p", class_="m-c-name").get_text(strip=True)
        price = crypto_price.find("div", class_="table-price-class").get_text(strip=True)
        cryptos.append({
            "Όνομα": name,
            "Τιμή": price
        })

# Print cryptocurrencies
for crypto in cryptos:
    print(crypto)