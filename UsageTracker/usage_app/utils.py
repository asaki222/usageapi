from datetime import datetime

def decimal_to_price(decimal_number):
    price_str = f"${decimal_number:.2f}"
    return price_str


def convert_to_datetime(datetime_str, format='%Y-%m-%dT%H:%M:%S'):
    try:
        parsed_datetime = datetime.strptime(datetime_str, format)
        formatted_datetime = parsed_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        return formatted_datetime
    except ValueError:
        return None
