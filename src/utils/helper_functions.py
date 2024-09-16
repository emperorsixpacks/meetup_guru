from datetime import datetime


def format_date(input_date: datetime):
    return datetime.strptime(input_date, "%Y-%m-%d").date()


def formate_time(input_time: str):
    return datetime.strptime(input_time, "%H:%M").time()
