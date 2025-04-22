import asyncio
from database.model.news import News
from database.repository.news import insert_news
from database import init_db
from crawler import crawl
from util import kst_now


async def main_handler():
    # 테이블 초기화
    init_db()
    
    # now = kst_now()

    news_info = await crawl()
    # print("news_info", news_info)
    # for data_list in news_info.data_list:
    #     name, amount = news_info.keyword, 0
    #     for data in data_list:
    #         amount += 1
    #         news = News(
    #             keyword=news_info.keyword,
    #             link=data.link,
    #             title=data.title,
    #             platform=data.platform,
    #             publisher=data.publisher,
    #             image_url=data.image_url,
    #             published_at=data.published_at,
    #             preview_content=data.preview_content
    #         )
    #         if news_info.should_save:
    #             insert_news(news)

    # news_list = query_not_submitted_today_news(kst_now())
    # update_submit_news(news_list)


if __name__ == "__main__":
    asyncio.run(main_handler())
