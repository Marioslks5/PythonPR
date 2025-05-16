import requests
from bs4 import BeautifulSoup

class Cryptoscraper:
    url = "https://www.coinlore.com/"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    cryptos = []

    rows = soup.find_all("tr", attrs={"data-id": True})

    for row in rows[:10]:
        crypto_name = row.find("td", class_="currency-name")
        crypto_price_div = row.find("div", class_="table-price-class")
        change_24h = row.find("div", class_="h24_change")
        change_7d = row.find("div", class_="7d_change2")
        total_volume = row.find("td", class_="market-cap")
        h24_volume = row.find("div", class_="table-volume-class")

        if crypto_name and crypto_price_div:
            name = crypto_name.get_text(strip=True)
            price = crypto_price_div.get_text(strip=True)
            change24H = change_24h.get_text(strip=True)
            change7d = change_7d.get_text(strip=True)
            total_volume = total_volume.get_text(strip=True)
            h24_volume = h24_volume.get_text(strip=True)

            cryptos.append({
                "Name": name,
                "Price": price,
                "Change 24H": change24H,
                "Change 7D": change7d,
                "Total Volume": total_volume,
                "24H Volume": h24_volume

            })

    for crypto in cryptos:
        print(crypto)