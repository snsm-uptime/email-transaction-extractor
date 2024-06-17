from datetime import datetime


def date_to_str(dt: datetime) -> str:
    return dt.strftime("%m/%d/%Y")


def str_to_date(dt: str) -> datetime:
    return datetime.strptime(dt, '%Y-%m-%d')
