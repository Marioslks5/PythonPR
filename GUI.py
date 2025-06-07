import tkinter as tk
from tkinter import Toplevel, Label, Button, Frame, Scrollbar, messagebox, Canvas
from tkinter import ttk
from PIL import Image, ImageTk


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
    {"name": "BNB", "image": "BNB.jpg"},
    {"name": "Tether", "image": "Tether.jpg"},
    {"name": "Litecoin", "image": "litecoin.jpg"},
    {"name": "XRP", "image": "xrp.jpg"},
    {"name": "Dogecoin", "image": "Dogecoin.jpg"},
    {"name": "Shiba Inu", "image": "shibainu.jpg"},
]

selected_coin = tk.StringVar()
selected_coin.set("Select Cryptocurrency")

# === Custom Dropdown with Icons and Scrollbar ===
def open_dropdown():
    dropdown = Toplevel(root)
    dropdown.title("Select Coin")
    dropdown.geometry("250x300")

    canvas = Canvas(dropdown)
    scrollbar = Scrollbar(dropdown, orient="vertical", command=canvas.yview)
    scroll_frame = Frame(canvas)

    scroll_frame.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for coin in CRYPTO_LIST:
        # Load and resize image
        img = Image.open(coin["image"])
        img = img.resize((32, 32))
        photo = ImageTk.PhotoImage(img)

        coin["photo"] = photo  # keep reference

        def select(c=coin["name"]):
            selected_coin.set(c)
            dropdown.destroy()

        btn = Button(scroll_frame, text=coin["name"], image=photo, compound="left", command=select)
        btn.pack(pady=5, padx=5, anchor="w")

# === Top Buttons ===
top_frame = Frame(root)
top_frame.pack(pady=10)

def fetch_data():
    messagebox.showinfo("Info", "Fetch data functionality goes here.")

def export_data():
    messagebox.showinfo("Info", "Export data functionality goes here.")

Button(top_frame, text="Fetch Data", command=fetch_data).grid(row=0, column=0, padx=5)
Button(top_frame, text="Export CSV", command=export_data).grid(row=0, column=1, padx=5)

# === Dropdown Section ===
Label(root, textvariable=selected_coin, font=("Arial", 14)).pack(pady=10)
Button(root, text="Choose Coin", command=open_dropdown).pack()

def show_chart():
    messagebox.showinfo("Info", f"Plot chart for {selected_coin.get()} goes here.")

Button(root, text="Show Chart", command=show_chart).pack(pady=10)

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
