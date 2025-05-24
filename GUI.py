import tkinter as tk

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import scraper
import requests
from bs4 import BeautifulSoup
from tkinter import Toplevel, Label, Button, Frame, Scrollbar, messagebox, Canvas
from tkinter import ttk
from PIL import Image, ImageTk

cryptos = []

# Create main window
root = tk.Tk()
root.title("Crypto Dashboard with Images")
root.geometry("1000x700")

# === Data ===
CRYPTO_LIST = [
    {"name": "Bitcoin", "image": "Bitcoin.jpg"},
    {"name": "Ethereum", "image": "ethereum.jpg"},
    {"name": "Cardano", "image": "cardano.jpg"},
    {"name": "Solana", "image": "Solana.jpg"},
    {"name": "Binance CoinBNB", "image": "BNB.jpg"},
    {"name": "Tether", "image": "Tether.jpg"},
    {"name": "USD CoinUSDC", "image": "USDC.jpg"},
    {"name": "XRP", "image": "xrp.jpg"},
    {"name": "Dogecoin", "image": "Dogecoin.jpg"},
    {"name": "Lido Staked EtherSTETH", "image": "STETH.jpg"},
]

COIN_IMAGES = {}
for coin in CRYPTO_LIST:
    try:
        img = Image.open(coin["image"]).resize((32, 32))
        COIN_IMAGES[coin["name"]] = ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error: {e}")

selected_coin = tk.StringVar()
selected_coin.set("Select Cryptocurrency")

# === Custom Dropdown with Icons and Scrollbar ===
def open_dropdown():
    dropdown = Toplevel(root)
    dropdown.title("Select Coin")
    dropdown.geometry("250x350")

    canvas = Canvas(dropdown)
    scrollbar = Scrollbar(dropdown, orient="vertical", command=canvas.yview)
    scroll_frame = Frame(canvas)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def select_all():
        selected_coin.set("Select Cryptocurrency")
        dropdown.destroy()
        fetch_data()

    all_btn = Button(scroll_frame, text="All Cryptocurrencies", command=select_all)
    all_btn.pack(pady=5, padx=5, anchor="w")

    for coin in CRYPTO_LIST:
        photo = COIN_IMAGES.get(coin["name"])

        def select(c=coin["name"]):
            selected_coin.set(c)
            dropdown.destroy()
            fetch_data()

        btn = Button(scroll_frame, text=coin["name"], image=photo, compound="left", command=select)
        btn.pack(pady=5, padx=5, anchor="w")


# === Top Buttons ===
top_frame = Frame(root)
top_frame.pack(pady=10)

def fetch_data():
    url = "https://www.coinlore.com/"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        rows = soup.find_all("tr", attrs={"data-id": True})
        cryptos.clear()

        for row in rows[:10]:
            name_cell = row.find("td", class_="currency-name")
            price = row.find("div", class_="table-price-class")
            change_24h = row.find("div", class_="h24_change")
            change_7d = row.find("div", class_="7d_change2")
            total_volume = row.find("td", class_="market-cap")
            h24_volume = row.find("div", class_="table-volume-class")

            if name_cell and price:
                name = name_cell.get_text(strip=True)
                symbol = name[-3:].lower()
                cryptos.append({
                    "Name": name,
                    "Symbol": symbol,
                    "Price": price.get_text(strip=True),
                    "Change 24H": change_24h.get_text(strip=True),
                    "Change 7D": change_7d.get_text(strip=True),
                    "Total Volume": total_volume.get_text(strip=True),
                    "24H Volume": h24_volume.get_text(strip=True),
                })

        tree.delete(*tree.get_children())
        for crypto in cryptos:
            if selected_coin.get() == "Select Cryptocurrency" or crypto["Name"].startswith(selected_coin.get()):
                tree.insert("", tk.END, values=(
                    crypto["Name"],
                    crypto["Price"],
                    crypto["Change 24H"],
                    crypto["Change 7D"],
                    crypto["Total Volume"],
                    crypto["24H Volume"]
                ))

        messagebox.showinfo("Success", "Data fetched successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch data:\n{e}")



def export_data():
    def update_csv(filename="cryptos.csv"):
        crypto = scraper.Cryptoscraper()
        crypto.scrape_data()

        new_data = pd.DataFrame(crypto.cryptos)

        if os.path.exists(filename):
            old_data = pd.read_csv(filename)
            combined = pd.concat([old_data, new_data], ignore_index=True)
            combined = combined.drop_duplicates(subset=["Name", "Price"], keep="last")
        else:
            combined = new_data

        combined.to_csv(filename, index=False)

    def load_data(filename="cryptos.csv"):
        if os.path.exists(filename):
            df = pd.read_csv(filename)
            return df
        else:
            return pd.DataFrame()

    def display_crypto_data(df):
        if df.empty:
            print("Δεν υπάρχουν δεδομένα για εμφάνιση.")
            return

        try:
            print("\nΔεδομένα Κρυπτονομισμάτων:\n")
            print(df[['Name', 'Price', 'Change 24H', 'Change 7D', 'Total Volume', '24H Volume']]
                  .drop_duplicates(subset=["Name"], keep="last").to_string(index=False))
        except KeyError as e:
            print("Σφάλμα στο αρχείο", e)

    try:
        update_csv()
        df = load_data()
        display_crypto_data(df)
        messagebox.showinfo("Επιτυχία", "Τα δεδομένα αποθηκεύτηκαν επιτυχώς στο cryptos.csv.")
    except Exception as e:
        messagebox.showerror("Σφάλμα", f"Πρόβλημα κατά την αποθήκευση: {e}")



Button(top_frame, text="Fetch Data", command=fetch_data).grid(row=0, column=0, padx=5)
Button(top_frame, text="Export CSV", command=export_data).grid(row=0, column=1, padx=5)

# === Dropdown Section ===
Label(root, textvariable=selected_coin, font=("Arial", 14)).pack(pady=10)
Button(root, text="Choose Coin", command=open_dropdown).pack()

def show_chart():
    import pandas as pd
    import matplotlib.pyplot as plt

    def load_and_clean_data(filename="cryptos.csv"):
        if not os.path.exists(filename):
            print("Το αρχείο δεν βρέθηκε.")
            return pd.DataFrame()

        df = pd.read_csv(filename)
        df = df.drop_duplicates(subset=["Name"], keep="last")

        df["Price"] = df["Price"].replace(r'[\$,]', '', regex=True).astype(float)
        df["Change 24H"] = df["Change 24H"].replace('%', '', regex=True).astype(float)
        df["Change 7D"] = df["Change 7D"].replace('%', '', regex=True).astype(float)
        df["Total Volume"] = df["Total Volume"].replace(r'[\$,A-Za-z\s]', '', regex=True).astype(float)

        return df

    def bar_chart(df):
        top5 = df.sort_values(by="Price", ascending=False).head(5)
        plt.figure(figsize=(8, 5))
        plt.bar(top5["Name"], top5["Price"], color='skyblue')
        plt.title("Τιμές των 5 κορυφαίων κρυπτονομισμάτων")
        plt.xlabel("Νόμισμα")
        plt.ylabel("Τιμή σε USD")
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

    def pie_chart(df):
        top5 = df.sort_values(by="Total Volume", ascending=False).head(5)
        plt.figure(figsize=(7, 7))
        plt.pie(top5["Total Volume"], labels=top5["Name"], autopct="%1.1f%%", startangle=140)
        plt.title("Κατανομή Κεφαλαιοποίησης Αγοράς")
        plt.axis("equal")
        plt.tight_layout()
        plt.show()

    def line_plot(df):
        top5 = df.head(5)
        x = top5["Name"]
        y1 = top5["Change 24H"]
        y2 = top5["Change 7D"]

        plt.figure(figsize=(9, 5))
        plt.plot(x, y1, marker='o', label="Μεταβολή 24ώρου (%)")
        plt.plot(x, y2, marker='s', label="Μεταβολή 7 ημερών (%)")
        plt.title("Μεταβολές Τιμών")
        plt.xlabel("Νόμισμα")
        plt.ylabel("Μεταβολή (%)")
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.show()

    df = load_and_clean_data("cryptos.csv")
    if df.empty:
        messagebox.showerror("Σφάλμα", "Δεν βρέθηκαν δεδομένα ή το αρχείο cryptos.csv λείπει.")
        return

    def show_selected_chart():
        chart_type = chart_var.get()
        if chart_type == "Bar Chart":
            bar_chart(df)
        elif chart_type == "Pie Chart":
            pie_chart(df)
        elif chart_type == "Line Plot":
            line_plot(df)

    chart_window = tk.Toplevel(root)
    chart_window.title("Επιλογή Γραφήματος")
    chart_window.geometry("300x200")

    chart_var = tk.StringVar(value="Bar Chart")

    tk.Label(chart_window, text="Διάλεξε τύπο γραφήματος:").pack(pady=10)
    tk.Radiobutton(chart_window, text="Bar Chart", variable=chart_var, value="Bar Chart").pack(anchor="w", padx=20)
    tk.Radiobutton(chart_window, text="Pie Chart", variable=chart_var, value="Pie Chart").pack(anchor="w", padx=20)
    tk.Radiobutton(chart_window, text="Line Plot", variable=chart_var, value="Line Plot").pack(anchor="w", padx=20)

    tk.Button(chart_window, text="Προβολή", command=show_selected_chart).pack(pady=10)


Button(root, text="Show Chart", command=show_chart).pack(pady=10)

#Chatbot button
#def chatbot():

# === Data Table ===
tree_frame = Frame(root)
tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)

tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
tree.pack(fill=tk.BOTH, expand=True)
tree_scroll.config(command=tree.yview)

# --- Define Columns ---
tree["columns"] = ("Name", "Price", "24h Change", "7d Change", "Market Cap", "Volume")
tree["show"] = "headings"
for col in tree["columns"]:
    tree.heading(col, text=col)
    tree.column(col, anchor=tk.CENTER, width=120)

# --- Sample rows ---
sample_data = [
    ("Bitcoin", "29000", "+2%", "+5%", "600B", "20B"),
    ("Ethereum", "1800", "+1%", "+3%", "200B", "10B"),
]

for row in sample_data:
    tree.insert("", tk.END, values=row)

# === Run App ===
root.mainloop()
