from datetime import datetime
from zoneinfo import ZoneInfo

def get_local_time(utc_time: datetime) -> datetime:
    return utc_time.astimezone(ZoneInfo("Europe/Sofia"))