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


class RequestConfig:
    NAVER_CLIENT_ID = os.environ["NAVER_CLIENT_ID"]
    NAVER_SECRET_KEY = os.environ["NAVER_SECRET_KEY"]
