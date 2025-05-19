import pytz
from uuid import uuid4
from datetime import datetime, timedelta, timezone
import httpx
from bs4 import BeautifulSoup
import boto3
from botocore.exceptions import BotoCoreError, NoCredentialsError
from config import S3Config
import mimetypes
import os
import io

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

def get_og_image_url(url: str) -> str:
    try:
        resp = httpx.get(url, timeout=5)
        if resp.status_code != 200:
            return None
        soup = BeautifulSoup(resp.text, 'html.parser')
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'):
            return og_image['content']
    except Exception:
        return None
    return None

def get_og_image(url: str) -> str:
    image_url = get_og_image_url(url)
    if not image_url:
        return None
    try:
        img_resp = httpx.get(image_url, timeout=10)
        if img_resp.status_code != 200:
            return None
        ext = mimetypes.guess_extension(img_resp.headers.get('content-type', '').split(';')[0]) or '.jpg'
        key = f'news-image/{uuid4().hex}{ext}'
        s3 = boto3.client(
            's3',
            aws_access_key_id=S3Config.S3_ACCESS_KEY,
            aws_secret_access_key=S3Config.S3_SECRET_KEY,
            region_name=S3Config.S3_REGION
        )
        s3.upload_fileobj(
            io.BytesIO(img_resp.content),
            S3Config.S3_BUCKET_NAME,
            key,
            ExtraArgs={'ContentType': img_resp.headers.get('content-type', 'image/jpeg')}
        )
        s3_url = f'https://{S3Config.S3_BUCKET_NAME}.s3.{S3Config.S3_REGION}.amazonaws.com/{key}'
        return s3_url
    except (BotoCoreError, NoCredentialsError, Exception) as e:
        return None