import asyncio
from database.model.news import News
from database.repository.news import insert_news
from database import init_db
from crawler import crawl


async def main_handler():
    # 테이블 초기화
    init_db()

    news_info_list = await crawl()
    for data_list in news_info_list:
        if data_list:
            for data in data_list.get("list"):
                news = News(
                    title=data.title,
                    publisher=data.publisher,
                    published_at=data.published_at,
                    link=data.link,
                    keyword=data_list.get("keyword"),
                    platform=data.platform,
                    image_url=data.image_url,
                )
                print(news)
                # insert_news(news)


if __name__ == "__main__":
    asyncio.run(main_handler())
