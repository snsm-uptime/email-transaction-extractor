from datetime import datetime


def date_to_str(dt: datetime) -> str:
    return dt.strftime("%m/%d/%Y")


def str_to_date(dt: str) -> datetime:
    return datetime.strptime(dt, '%Y-%m-%d')


def parse_end_date(date_str: str) -> datetime:
    parsed_date = datetime.strptime(date_str, '%Y-%m-%d')
    current_time = datetime.now()
    if parsed_date > current_time:
        return current_time
    return parsed_date
