import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, Frame, Canvas, Scrollbar, Label, Button
from PIL import Image, ImageTk
import re

# Import your existing modules
import scraper
import chatbot
import visual
import Datatel

# Global variables
cryptos = []
coin_images = {}
selected_coin = None
tree = None
root = None

# Cryptocurrency list for images
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


def load_coin_images():
    """Load cryptocurrency images for the dropdown"""
    global coin_images
    for coin in CRYPTO_LIST:
        try:
            img = Image.open(coin["image"]).resize((32, 32))
            coin_images[coin["name"]] = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading image {coin['image']}: {e}")


def update_table():
    """Update the data table with current crypto data"""
    global tree, cryptos
    tree.delete(*tree.get_children())

    # Get data from scraper module
    cryptos = scraper.cryptos
    selected_name = selected_coin.get()

    for crypto in cryptos:
        if selected_name == "Select Cryptocurrency" or crypto["Name"].startswith(selected_name):
            tree.insert("", tk.END, values=(
                crypto["Name"],
                crypto["Price"],
                crypto["Change 24H"],
                crypto["Change 7D"],
                crypto["Total Volume"],
                crypto["24H Volume"]
            ))


def fetch_data():
    """Fetch cryptocurrency data using scraper module"""
    try:
        scraper.scrape_data()
        update_table()
        messagebox.showinfo("Success", "Data fetched successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch data: {e}")


def export_data():
    """Export data using datatel module"""
    try:
        Datatel.update_csv()
        df = Datatel.load_data()
        Datatel.display_crypto_data(df)
        messagebox.showinfo("Success", "Data exported successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export data: {e}")


def show_chart_selector():
    """Open chart selection window using visual module"""
    if not scraper.cryptos:
        messagebox.showwarning("Warning", "No data available. Please fetch data first.")
        return

    chart_window = Toplevel(root)
    chart_window.title("Select Chart Type")
    chart_window.geometry("300x200")
    chart_window.grab_set()
    chart_window.transient(root)

    chart_var = tk.StringVar(value="Bar Chart")

    Label(chart_window, text="Choose chart type:", font=("Arial", 12)).pack(pady=15)

    tk.Radiobutton(chart_window, text="Bar Chart - Top 5 Prices",
                   variable=chart_var, value="Bar Chart").pack(anchor="w", padx=30)
    tk.Radiobutton(chart_window, text="Pie Chart - Market Cap Distribution",
                   variable=chart_var, value="Pie Chart").pack(anchor="w", padx=30)
    tk.Radiobutton(chart_window, text="Line Plot - Price Changes",
                   variable=chart_var, value="Line Plot").pack(anchor="w", padx=30)

    def show_selected_chart():
        chart_type = chart_var.get()
        try:
            df = visual.load_and_clean_data()
            if df.empty:
                messagebox.showerror("Error", "No data found or cryptos.csv file is missing.")
                return

            if chart_type == "Bar Chart":
                visual.bar_chart(df)
            elif chart_type == "Pie Chart":
                visual.pie_chart(df)
            elif chart_type == "Line Plot":
                visual.line_plot(df)
            chart_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to display chart: {e}")

    Button(chart_window, text="Show Chart", command=show_selected_chart,
           bg="#4CAF50", fg="white", font=("Arial", 10)).pack(pady=15)


def open_chatbot():
    """Open chatbot interface"""
    # Ensure we have fresh data
    scraper.scrape_data()

    chat_window = Toplevel(root)
    chat_window.title("CryptoBot")
    chat_window.geometry("500x400")
    chat_window.grab_set()

    # Chat display area
    chat_frame = Frame(chat_window)
    chat_frame.pack(fill="both", expand=True, padx=10, pady=10)

    chat_history = tk.Text(chat_frame, wrap="word", state="disabled", bg="#f0f0f0")
    scrollbar = tk.Scrollbar(chat_frame, command=chat_history.yview)
    chat_history.configure(yscrollcommand=scrollbar.set)

    chat_history.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Input area
    input_frame = Frame(chat_window)
    input_frame.pack(fill="x", padx=10, pady=(0, 10))

    user_input = tk.Entry(input_frame, font=("Arial", 10))
    user_input.pack(side="left", fill="x", expand=True, padx=(0, 5))

    def add_message(sender, message):
        chat_history.config(state="normal")
        chat_history.insert(tk.END, f"{sender}: {message}\n\n")
        chat_history.config(state="disabled")
        chat_history.see(tk.END)

    def send_message():
        message = user_input.get().strip()
        if not message:
            return

        add_message("You", message)
        user_input.delete(0, tk.END)

        # Get response from chatbot module
        try:
            response = chatbot.generate_response(message)
            add_message("CryptoBot", response)
        except Exception as e:
            add_message("CryptoBot", f"Sorry, I encountered an error: {e}")

    def on_enter(event):
        send_message()

    user_input.bind("<Return>", on_enter)
    Button(input_frame, text="Send", command=send_message,
           bg="#2196F3", fg="white").pack(side="right")

    # Welcome message
    add_message("CryptoBot",
                "Hello! How can I help you with cryptocurrency information? You can ask about prices, changes, volumes, or type 'help' for more options.")


def open_coin_dropdown():
    """Open dropdown for coin selection"""
    dropdown = Toplevel(root)
    dropdown.title("Select Cryptocurrency")
    dropdown.geometry("250x400")
    dropdown.grab_set()

    canvas = Canvas(dropdown)
    scrollbar = Scrollbar(dropdown, orient="vertical", command=canvas.yview)
    scroll_frame = Frame(canvas)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def select_coin(coin_name):
        selected_coin.set(coin_name)
        dropdown.destroy()
        update_table()

    # "All" option
    Button(scroll_frame, text="All Cryptocurrencies",
           command=lambda: select_coin("Select Cryptocurrency")).pack(pady=5, padx=5, fill="x")

    # Individual coins with images
    for coin in CRYPTO_LIST:
        photo = coin_images.get(coin["name"])
        Button(scroll_frame, text=coin["name"], image=photo, compound="left",
               command=lambda c=coin["name"]: select_coin(c)).pack(pady=2, padx=5, fill="x")


def create_data_table():
    """Create the main data display table"""
    global tree

    # Table frame
    table_frame = Frame(root)
    table_frame.pack(pady=10, fill="both", expand=True)

    # Scrollbar for table
    table_scroll = tk.Scrollbar(table_frame)
    table_scroll.pack(side="right", fill="y")

    # Create treeview
    tree = ttk.Treeview(table_frame, yscrollcommand=table_scroll.set)
    tree.pack(fill="both", expand=True)
    table_scroll.config(command=tree.yview)

    # Define columns
    tree["columns"] = ("Name", "Price", "24h Change", "7d Change", "Market Cap", "Volume")
    tree["show"] = "headings"

    # Configure column headings and widths
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=120)

    # Add sample data
    sample_data = [
        ("Bitcoin", "$29,000", "+2.5%", "+5.2%", "$600B", "$20B"),
        ("Ethereum", "$1,800", "+1.8%", "+3.1%", "$200B", "$10B"),
    ]

    for row in sample_data:
        tree.insert("", tk.END, values=row)


def setup_main_window():
    """Initialize and setup the main application window"""
    global root, selected_coin

    root = tk.Tk()
    root.title("Crypto Dashboard")
    root.geometry("1000x700")
    root.configure(bg="#f5f5f5")

    selected_coin = tk.StringVar(value="Select Cryptocurrency")

    # Load images
    load_coin_images()

    # Header
    header_label = Label(root, text="Cryptocurrency Dashboard",
                         font=("Arial", 16, "bold"), bg="#f5f5f5")
    header_label.pack(pady=10)

    # Control buttons
    button_frame = Frame(root, bg="#f5f5f5")
    button_frame.pack(pady=10)

    Button(button_frame, text="Fetch Data", command=fetch_data,
           bg="#4CAF50", fg="white", font=("Arial", 10)).grid(row=0, column=0, padx=5)
    Button(button_frame, text="Export CSV", command=export_data,
           bg="#FF9800", fg="white", font=("Arial", 10)).grid(row=0, column=1, padx=5)
    Button(button_frame, text="Show Charts", command=show_chart_selector,
           bg="#9C27B0", fg="white", font=("Arial", 10)).grid(row=0, column=2, padx=5)
    Button(button_frame, text="Chatbot", command=open_chatbot,
           bg="#2196F3", fg="white", font=("Arial", 10)).grid(row=0, column=3, padx=5)

    # Coin selection
    selection_frame = Frame(root, bg="#f5f5f5")
    selection_frame.pack(pady=10)

    Label(selection_frame, textvariable=selected_coin, font=("Arial", 12),
          bg="#f5f5f5").pack()
    Button(selection_frame, text="Choose Cryptocurrency", command=open_coin_dropdown,
           bg="#607D8B", fg="white", font=("Arial", 10)).pack(pady=5)

    # Data table
    create_data_table()


def run_application():
    """Main function to run the application"""
    setup_main_window()
    root.mainloop()


if __name__ == "__main__":
    run_application()