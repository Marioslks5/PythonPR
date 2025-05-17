import re

from scraper import Cryptoscraper


scraper = Cryptoscraper()
scraper.scrape_data()

SUPPORTED_COINS = [
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


patterns = [
    r"(τιμή|κοστίζει|αξία|πόσο κάνει)",
    r"(μεταβολή|άνοδος|πτώση).*(24|24ωρο)",
    r"(μεταβολή|άνοδος|πτώση).*(7|εβδομάδα)",
    r"(όγκος|συναλλαγές).*(24|24ωρο)",
    r"(σύνολο|συνολικός|όγκος)",
    r"(ποια.*νομίσματα|λίστα|διαθέσιμα)",
    r"(βοήθεια|τι μπορώ|οδηγίες|commands)",
    r"(άλλαξε|διάλεξε).*νόμισμα",
    r"(ποιο|τι).*σύμβολο"
]

def chatbot(scraper):
    print("Chatbot: Γειά! Με τι μπορώ να σε βοηθήσω? (γράψε exit για έξοδο)")
    while True:
        user_input = input("Εσύ: ")
        if user_input.lower() in ["exit","quit"]:
            break
        response = generate_response(user_input, scraper)
        print("CryptoBot:", response)

def extract_coin(user_input):
    user_input = user_input.lower()
    for name, symbol in SUPPORTED_COINS:
        if name in user_input or symbol in user_input:
            return symbol
    return None

def generate_response(user_input, scraper):
    user_input = user_input.lower()

    # Πρώτα ελέγχουμε για ερωτήσεις που δεν χρειάζονται νόμισμα
    if re.search(r"(ποια.*νομίσματα|λίστα|διαθέσιμα|υποστηρίζονται)", user_input):
        return "Υποστηριζόμενα νομίσματα: BitcoinBTC, EthereumETH, TetherUSDT, XRPXRP, Binance CoinBNB, SolanaSOL, USD CoinUSDC, DogecoinDOGE, CardanoADA, TRONTRX"

    if re.search(r"(βοήθεια|τι μπορώ|οδηγίες|commands)", user_input):
        return "Μπορείς να ρωτήσεις για τιμή, μεταβολή 24ωρου ή 7 ημερών, όγκο, διαθέσιμα νομίσματα, σύμβολο, κ.α."

    if re.search(r"(άλλαξε|διάλεξε).*νόμισμα", user_input):
        return "Πες μου το σύμβολο του νομίσματος που σε ενδιαφέρει (π.χ. BTC, ETH)."

    # Τώρα χρειάζεται νόμισμα — το εντοπίζουμε:
    coin = extract_coin(user_input)

    if not coin:
        return "Παρακαλώ πες μου για ποιο νόμισμα ενδιαφέρεσαι (π.χ. btc, eth)."

    data = scraper.get_coin_data(coin)
    if not data:
        return "Δεν βρήκα δεδομένα για το συγκεκριμένο νόμισμα."

    # Ανίχνευση pattern που χρειάζεται νόμισμα
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


if __name__ == "__main__":
    # Run the chatbot
    chatbot(scraper)
