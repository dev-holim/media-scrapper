import asyncio

from crawler.api.youtube import YouTubeCrawler
from database import init_db
from database.model.youtube import Youtube
from database.repository.youtube import insert_youtube


async def main_handler():
    # 테이블 초기화
    init_db()

    youtube_list = YouTubeCrawler().fetch()

    for youtube in youtube_list:
        youtube = Youtube(
            title=youtube.get("title"),
            author=youtube.get("author"),
            url_path=youtube.get("url"),
            share_path=youtube.get("embed_url"),
            image_path=youtube.get("thumbnail_url"),
            youtube_at=youtube.get("published_at"),
        )
        insert_youtube(youtube)


if __name__ == "__main__":
    asyncio.run(main_handler())