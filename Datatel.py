import os
import pandas as pd
import scraper  

def update_csv(filename="cryptos.csv"):
    scrape_data()
    new_data=
    pd.DataFrame(scraper.cryptos)

    if os.path.exists(filename):
        old_data = pd.read_csv(filename)
        combined = pd.concat([old_data, new_data], ignore_index=True)
        combined = combined.drop_duplicates(subset=["Name", "Price"], keep="last")
    else:
        combined = new_data

    combined.to_csv(filename, index=False)
    print(f"Τα δεδομένα αποθηκεύτηκαν επιτυχώς.")

def load_data(filename="cryptos.csv"):
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        print(f"Οι εγγραφές φορτώθηκαν απο το αρχείο επιτυχώς.")
        return df
    else:
        print("Το αρχείο δεν βρέθηκε.")
        return pd.DataFrame()

def display_crypto_data(df):
    if df.empty:
        print("Δεν υπάρχουν δεδομένα για εμφάνιση.")
        return

    try:
        print("\nΔεδομένα Κρυπτονομισμάτων:\n")
        print(df[['Name', 'Price', 'Change 24H', 'Change 7D', 'Total Volume', '24H Volume']].drop_duplicates(subset=["Name"], keep="last").to_string(index=False))
    except KeyError as e:
        print("Σφάλμα στο αρχείο", e)

if __name__ == "__main__":
    update_csv()
    df = load_data()
    display_crypto_data(df)
