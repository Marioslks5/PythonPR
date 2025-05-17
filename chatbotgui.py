import tkinter as tk
from tkinter import scrolledtext
from chatbot import CryptoChatbot
from scraper import Cryptoscraper

class CryptoChatGUI:
    def __init__(self, root, bot):
        self.bot = bot
        root.title("Crypto Chatbot")

        # Chat display (scrollable)
        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', width=60, height=20)
        self.chat_area.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Entry box for user input
        self.entry = tk.Entry(root, width=50)
        self.entry.grid(row=1, column=0, padx=10, pady=10)
        self.entry.bind("<Return>", self.send_message)  # Press Enter to send

        # Send button
        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

        # Show greeting
        self.display_message("CryptoBot", "Γειά! Με τι μπορώ να σε βοηθήσω; (γράψε exit για έξοδο)")

    def display_message(self, sender, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)  # Auto scroll to bottom

    def send_message(self, event=None):
        user_input = self.entry.get().strip()
        if not user_input:
            return

        # Display user message
        self.display_message("Εσύ", user_input)
        self.entry.delete(0, tk.END)

        if user_input.lower() in ["exit", "quit"]:
            self.display_message("CryptoBot", "Αντίο! Να έχεις μια καλή μέρα!")
            self.entry.config(state='disabled')
            self.send_button.config(state='disabled')
            return

        # Get bot response
        response = self.bot.generate_response(user_input)
        self.display_message("CryptoBot", response)


if __name__ == "__main__":
    scraper = Cryptoscraper()
    scraper.scrape_data()

    bot = CryptoChatbot(scraper)

    root = tk.Tk()
    gui = CryptoChatGUI(root, bot)
    root.mainloop()
