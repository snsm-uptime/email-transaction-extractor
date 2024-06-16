from datetime import datetime, timedelta


class DateRange:
    def __init__(self, start_date: datetime = None, end_date: datetime = None, days_ago: int = None):
        if days_ago is not None:
            end_date = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
            start_date = (datetime.now() - timedelta(days=days_ago)
                          ).replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            if start_date is None or end_date is None:
                raise ValueError(
                    "Either 'start_date' and 'end_date' or 'days_ago' must be provided.")
            self.start_date = start_date.replace(
                hour=0, minute=0, second=0, microsecond=0)
            self.end_date = end_date.replace(
                hour=23, minute=59, second=59, microsecond=999999)

    def duration(self) -> int:
        return (self.end_date - self.start_date).days

    def __repr__(self):
        return f"DateRange(start_date={self.start_date}, end_date={self.end_date}, duration={self.duration()} days)"
