import pandas as pd
import matplotlib.pyplot as plt
import os

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

if __name__ == "__main__":
    df = load_and_clean_data()
    if not df.empty:
        bar_chart(df)
        pie_chart(df)
        line_plot(df)
