import requests
from bs4 import BeautifulSoup

url = "https://www.coinlore.com/"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# List for storing cryptocurrencies
cryptos = []

rows = soup.find_all("tr", attrs={"data-id": True})

# Extracting data from each row
for row in rows[:10]:  # Πρώτα 10 νομίσματα
    crypto_name = row.find("td", class_= "currency-name")
    crypto_price = row.find("td", class_="price_td_p")

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