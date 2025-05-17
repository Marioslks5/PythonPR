import re

class CryptoChatbot:
    def __init__(self, scraper):
        self.scraper = scraper
        self.SUPPORTED_COINS = [
            ("bitcoin", "btc"),
            ("ethereum", "eth"),
            ("tether", "usdt"),
            ("xrp", "xrp"),
            ("binance coin", "bnb"),
            ("solana", "sol"),
            ("usd coin", "usdc"),
            ("dogecoin", "doge"),
            ("cardano", "ada"),
            ("tron", "trx")
        ]

    def extract_coin(self, user_input):
        user_input = user_input.lower()
        for name, symbol in self.SUPPORTED_COINS:
            if name in user_input or symbol in user_input:
                return symbol
        return None

    def generate_response(self, user_input):
        user_input = user_input.lower()

        if re.search(r"(ποια.*νομίσματα|λίστα|διαθέσιμα|υποστηρίζονται)", user_input):
            coins_list = ", ".join([f"{name.capitalize()}({symbol.upper()})" for name, symbol in self.SUPPORTED_COINS])
            return f"Υποστηριζόμενα νομίσματα: {coins_list}"

        if re.search(r"(βοήθεια|τι μπορώ|οδηγίες|commands)", user_input):
            return "Μπορείς να ρωτήσεις για τιμή, μεταβολή 24ωρου ή 7 ημερών, όγκο, διαθέσιμα νομίσματα, σύμβολο, κ.α."

        if re.search(r"(άλλαξε|διάλεξε).*νόμισμα", user_input):
            return "Πες μου το σύμβολο του νομίσματος που σε ενδιαφέρει (π.χ. BTC, ETH)."

        coin = self.extract_coin(user_input)
        if not coin:
            return "Παρακαλώ πες μου για ποιο νόμισμα ενδιαφέρεσαι (π.χ. btc, eth)."

        data = self.scraper.get_coin_data(coin)
        if not data:
            return "Δεν βρήκα δεδομένα για το συγκεκριμένο νόμισμα."

        if re.search(r"(τιμή|κοστίζει|αξία|πόσο κάνει)", user_input):
            return f"Η τιμή του {coin.upper()} είναι {data['Price']}."

        elif re.search(r"(μεταβολή|άνοδος|πτώση).*(24|24ωρο)", user_input):
            return f"Η μεταβολή 24ώρου του {coin.upper()} είναι {data['Change 24H']}."

        elif re.search(r"(μεταβολή|άνοδος|πτώση).*(7|εβδομάδα)", user_input):
            return f"Η μεταβολή 7 ημερών του {coin.upper()} είναι {data['Change 7D']}."

        elif re.search(r"(όγκος|συναλλαγές).*(24|24ωρο)", user_input):
            return f"Ο 24ώρος όγκος συναλλαγών του {coin.upper()} είναι {data['24H Volume']}."

        elif re.search(r"(σύνολο|συνολικός|όγκος)", user_input):
            return f"Ο συνολικός όγκος του {coin.upper()} είναι {data['Total Volume']}."

        elif re.search(r"(ποιο|τι).*σύμβολο", user_input):
            return f"Το σύμβολο του {coin.upper()} είναι {data['Symbol'].upper()}."

        else:
            return "Δεν κατάλαβα την ερώτησή σου. Δοκίμασε ξανά ή γράψε 'βοήθεια'."