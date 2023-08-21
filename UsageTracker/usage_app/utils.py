from datetime import datetime

def decimal_to_price(decimal_number):
    price_str = f"${decimal_number:.2f}"
    return price_str
