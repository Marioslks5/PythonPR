import schedule
import time
from datetime import datetime
from scraper import scrape_data, save_csv


def run_scrape(market_name):
    print(f"Έναρξη scraping για {market_name} στις {datetime.now()}")
    scrape_data()

    timestamp = datetime.now()
    filename = f"cryptos_{market_name}_{timestamp}.csv"

    save_csv(filename="cryptos_scheduled.csv")
    print(f" {market_name} scraping ολοκληρώθηκε: {filename}")


#ΠΡΟΓΡΑΜΜΑΤΙΣΜΟΣ SCRAPING
schedule.every().day.at("09:00").do(run_scrape, "EU-OPEN")
schedule.every().day.at("14:30").do(run_scrape, "US-OPEN")
schedule.every().day.at("15:00").do(run_scrape, "US-EU-OVERLAP")

while True:
    schedule.run_pending()
    time.sleep(60)