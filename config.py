import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

class DatabaseConfig:
    _HOST = os.environ['DATABASE_HOST']
    _PORT = os.environ['DATABASE_PORT']
    _NAME = os.environ['DATABASE_NAME']

    _USER_NAME = os.environ['USER_NAME']
    _PASSWORD = os.environ['USER_PASSWORD']

    URL = f"postgresql+psycopg2://{_USER_NAME}:{_PASSWORD}@{_HOST}:{_PORT}/{_NAME}"


class NaverConfig:
    CLIENT_ID = os.environ["NAVER_CLIENT_ID"]
    SECRET_KEY = os.environ["NAVER_SECRET_KEY"]

class GoogleConfig:
    API_KEY = os.environ["GOOGLE_API_KEY"]

class S3Config:
    S3_ACCESS_KEY = os.environ["S3_ACCESS_KEY"]
    S3_SECRET_KEY = os.environ["S3_SECRET_KEY"]
    S3_BUCKET_NAME = os.environ["S3_BUCKET_NAME"]
    S3_REGION = os.environ.get("S3_REGION", "ap-northeast-2")
