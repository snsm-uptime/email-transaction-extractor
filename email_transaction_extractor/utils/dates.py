from datetime import datetime, timedelta
from pydantic import BaseModel, model_validator


class DateRange(BaseModel):
    start_date: datetime = None
    end_date: datetime = None
    days_ago: int = None

    @model_validator(mode='before')
    def set_dates(cls, values):
        days_ago = values.get('days_ago')
        # TODO: str_to_datetime for these
        start_date = values.get('start_date', datetime.now())
        end_date = values.get('end_date', datetime.now())

        if days_ago is not None:
            end_date = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
            start_date = (datetime.now() - timedelta(days=days_ago)
                          ).replace(hour=0, minute=0, second=0, microsecond=0)
            values['start_date'] = start_date
            values['end_date'] = end_date
        else:
            if start_date is None or end_date is None:
                raise ValueError(
                    "Either 'start_date' and 'end_date' or 'days_ago' must be provided.")
            values['start_date'] = start_date.replace(
                hour=0, minute=0, second=0, microsecond=0)
            values['end_date'] = end_date.replace(
                hour=23, minute=59, second=59, microsecond=999999)
        return values

    def duration(self) -> int:
        return (self.end_date - self.start_date).days

    def __str__(self):
        return f"Date range = {self.start_date:%B %d, %Y} to {self.end_date:%B %d, %Y}"
