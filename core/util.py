import pytz
from uuid import uuid4
from datetime import datetime, timedelta, timezone


def kst_now():
    return datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Seoul'))
    # return datetime.utcnow() + timedelta(hours=9)

def parse_datetime_kst(value, is_gmt:bool=False) -> datetime:
    format_ = '%a, %d %b %Y %H:%M:%S GMT' if is_gmt else '%a, %d %b %Y %H:%M:%S'
    dt = value if isinstance(value, datetime) else datetime.strptime(value, format_)

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    return dt.astimezone(pytz.timezone('Asia/Seoul'))
    # return dt.astimezone(timezone(timedelta(hours=9)))


def is_outdated_kst(kst_last_at, ago:int, is_hour:bool=True) -> bool:
    if is_hour:
        ago = ago * 60
    return kst_last_at < kst_now() - timedelta(minutes=ago)

def generate_random_str():
    uid = str(uuid4())

    return uid.split('-')[0]

def cron_log(message: str):
    print(f"[{kst_now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")