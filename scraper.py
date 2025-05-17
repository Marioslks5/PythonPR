import requests
from bs4 import BeautifulSoup
import pandas as pd

# Global variable to store cryptocurrency data
cryptos = []

def scrape_data():
    url = "https://www.coinlore.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    global cryptos
    cryptos = []  # Reset the list before scraping new data

    rows = soup.find_all("tr", attrs={"data-id": True})

    for row in rows[:10]:
        crypto_name = row.find("td", class_="currency-name")
        crypto_price = row.find("div", class_="table-price-class")
        change_24h = row.find("div", class_="h24_change")
        change_7d = row.find("div", class_="7d_change2")
        total_volume = row.find("td", class_="market-cap")
        h24_volume = row.find("div", class_="table-volume-class")

        if crypto_name and crypto_price:
            name = crypto_name.get_text(strip=True)
            symbol = name[-3:].lower()
            price = crypto_price.get_text(strip=True)
            change24h = change_24h.get_text(strip=True)
            change7d = change_7d.get_text(strip=True)
            total_volume = total_volume.get_text(strip=True)
            h24_volume = h24_volume.get_text(strip=True)

            cryptos.append({
                "Name": name,
                "Symbol": symbol,
                "Price": price,
                "Change 24H": change24h,
                "Change 7D": change7d,
                "Total Volume": total_volume,
                "24H Volume": h24_volume
            })

def print_data():
    for crypto in cryptos:
        print(crypto)

def get_coin_names():
    for crypto in cryptos:
        print(crypto["Symbol"])

def get_coin_data(symbol):
    for crypto in cryptos:
        if crypto["Symbol"] == symbol:
            return crypto
    return None

def save_csv(filename="cryptos.csv"):
    df = pd.DataFrame(cryptos)
    df.to_csv(filename, index=False)

if __name__ == "__main__":
    scrape_data()
    print(get_coin_data('btc'))
    get_coin_names()
    save_csv()