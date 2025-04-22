from uuid import uuid4
from datetime import datetime, timedelta


def kst_now():
    now = datetime.utcnow() + timedelta(hours=9)

    return now


def generate_random_str():
    uid = str(uuid4())

    return uid.split('-')[0]

def cron_log(message: str):
    print(f"[{kst_now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")