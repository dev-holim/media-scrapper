from datetime import datetime, timedelta
from typing import List

from sqlalchemy import and_

from database import session_scope
from database.model.news import News
from sqlalchemy.exc import IntegrityError


def insert_news_list(news_list: List[News]):
    with session_scope() as session:
        for i in news_list:
            try:
                session.add(i)
                session.commit()

            except IntegrityError:
                session.rollback()
                continue


def insert_news(news: News):
    with session_scope() as session:
        try:
            session.add(news)
            session.commit()

        except IntegrityError:
            print('EXIST', news.keyword, news.platform, news.title)
            session.rollback()


def query_not_submitted_today_news(today: datetime):
    yesterday = (today - timedelta(days=1)).date()

    with session_scope() as session:
        result = session.query(News).filter(
            and_(
                News.is_active == False,
                yesterday <= News.published_at
            )
        ).all()

    return result


def update_submit_news(news_list: List[News]):
    with session_scope() as session:
        for news in news_list:
            session.query(News) \
                .filter(News.id == news.id) \
                .update({"is_active": True})
