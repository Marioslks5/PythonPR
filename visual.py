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
    bars = plt.bar(top5["Name"], top5["Price"], color='skyblue', label="Τιμή σε USD")
    plt.title("Τιμές των 5 Κορυφαίων Κρυπτονομισμάτων")
    plt.xlabel("Νόμισμα")
    plt.ylabel("Τιμή σε USD")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend()
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, height, f'{height:.2f}', ha='center', va='bottom')
    plt.tight_layout()
    plt.show()

def pie_chart(df):
    top5 = df.sort_values(by="Total Volume", ascending=False).head(5)
    plt.figure(figsize=(7, 7))
    wedges, texts, autotexts = plt.pie(
        top5["Total Volume"],
        labels=top5["Name"],
        autopct="%1.1f%%",
        startangle=140
    )
    plt.title("Κατανομή Όγκου Συναλλαγών των 5 Κορυφαίων Κρυπτονομισμάτων")
    plt.axis("equal")
    plt.legend(wedges, top5["Name"], title="Νομίσματα", loc="center left", bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.show()

def line_plot(df):
    top5 = df.head(5)
    x = top5["Name"]
    y1 = top5["Change 24H"]
    y2 = top5["Change 7D"]

    plt.figure(figsize=(9, 5))
    plt.plot(x, y1, marker='o', label="Μεταβολή 24ώρου (%)", color='blue')
    plt.plot(x, y2, marker='s', label="Μεταβολή 7 ημερών (%)", color='green')
    plt.title("Μεταβολές Τιμών των 5 Κορυφαίων Κρυπτονομισμάτων")
    plt.xlabel("Νόμισμα")
    plt.ylabel("Μεταβολή (%)")
    plt.legend(title="Χρονικό Διάστημα")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    df = load_and_clean_data()
    if not df.empty:
        bar_chart(df)
        pie_chart(df)
        line_plot(df)
