from datetime import datetime


def is_valid_date(date_string, format):
    try:
        datetime.strptime(date_string, format)
        return True
    except ValueError:
        return False
