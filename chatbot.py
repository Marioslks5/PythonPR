import re
from scraper import scrape_data, get_coin_data

# Define supported coins as a global constant
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

def extract_coin(user_input):

    user_input = user_input.lower()
    for name, symbol in SUPPORTED_COINS:
        if name in user_input or symbol in user_input:
            return symbol
    return None

def generate_response(user_input):

    user_input = user_input.lower()

    # Check for general queries
    if re.search(r"(ποιά.*νομίσματα|λίστα|διαθέσιμα|υποστηρίζονται)", user_input):
        coins_list = ", ".join([f"{name.capitalize()}({symbol.upper()})" for name, symbol in SUPPORTED_COINS])
        return f"Υποστηριζόμενα νομίσματα: {coins_list}"

    if re.search(r"(βοήθεια|τι μπορώ|οδηγίες|commands)", user_input):
        return"Μπορείς να ρωτήσεις για τιμή, μεταβολή 24ωρου ή 7 ημερών, όγκο, διαθέσιμα νομίσματα, σύμβολο, κ.α."

    if re.search(r"(άλλαξε|διάλεξε).*νόμισμα", user_input):
        return "Πες μου το σύμβολο του νομίσματος που σε ενδιαφέρει (π.χ. BTC, ETH)."

    # Extract coin and get data
    coin = extract_coin(user_input)
    if not coin:
        return "Δώσε έγκυρο νόμισμα (π.χ. btc, eth)."

    data = get_coin_data(coin)
    if not data:
        return "Δεν βρέθηκαν δεδομένα για το νόμισμα."

    # Handle specific queries
    if re.search(r"(τιμή|κοστίζει|αξία|πόσο κάνει)", user_input):
        return f"Η τιμή του {coin.upper()} είναι {data['Price']}."

    elif re.search(r"(μεταβολή|άνοδος|πτώση).*(24|24ωρο)", user_input):
        return f"Η μεταβολή 24ώρου του {coin.upper()} είναι {data['Change 24H']}."

    elif re.search(r"(μεταβολή|άνοδος|πτώση). *(7|εβδομάδα)", user_input):
        return f"Η μεταβολή 7 ημερών του {coin.upper()} είναι {data['Change 7D']}."

    elif re.search(r"(όγκος|συναλλαγές). *(24|24ωρο)", user_input):
        return f"Ο 24ώρος όγκος συναλλαγών του {coin.upper()} είναι {data['24H Volume']}."

    elif re.search(r"(σύνολο|συνολικός|όγκος)", user_input):
        return f"Ο συνολικός όγκος του {coin.upper()} είναι {data['Total Volume']}."

    elif re.search(r"(ποιο|τι).*σύμβολο", user_input):
        return f"Το σύμβολο του {coin.upper()} είναι {data['Symbol'].upper()}."

    else:
        return "Δεν κατάλαβα την ερώτησή σου. Δοκίμασε ξανά ή γράψε 'βοήθεια'."

def run_chatbot():
    # Initialize data
    scrape_data()
    
    print("CryptoChatbot: Γειά! Πώς μπορώ να σε βοηθήσω? ('exit' για έξοδο)")
    
    while True:
        user_input = input("Εσύ: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        response = generate_response(user_input)
        print("CryptoBot:", response)

if __name__ == "__main__":
    run_chatbot()