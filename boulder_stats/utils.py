"""Helper functions."""
import pandas as pd

OPENING_TIME = "09:00"
CLOSING_TIME = "23:00"


def get_slots(date, opening_time=OPENING_TIME, closing_time=CLOSING_TIME):
    """Return date_range corresponding to slots that can be booked online."""
    if isinstance(date, str):
        date = pd.Timestamp(date).date()
    if isinstance(opening_time, str):
        opening_time = pd.Timestamp(opening_time).time()
    if isinstance(closing_time, str):
        closing_time = pd.Timestamp(closing_time).time()
    start = pd.Timestamp.combine(date=date, time=opening_time)
    end = pd.Timestamp.combine(date=date, time=closing_time)
    return pd.date_range(start=start, end=end, freq="0.5H")


assert all(get_slots("2020-10-28") == get_slots(pd.Timestamp("2020-10-28")))


def is_open(datetime):
    """Return weather datetime lies in the opening times or not."""
    dow = datetime.dayofweek
    time = datetime.time()
    earlier_days = {6, 7}
    start = pd.Timestamp("10:00" if dow not in earlier_days else "09:00").time()
    end = pd.Timestamp("22:00").time()
    return start <= time <= end


def is_future(datetime):
    """Return weather ``datetime`` lies in the future."""
    return datetime > pd.Timestamp.now()


def next_weekday(datetime, weekday):
    """Return date of next ``weekday``."""
    days_ahead = weekday - datetime.weekday()
    if days_ahead < 0:  # Target day already happened this week
        days_ahead += 7
    return datetime + pd.Timedelta(days=days_ahead)
