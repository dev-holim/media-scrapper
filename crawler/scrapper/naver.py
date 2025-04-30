from datetime import datetime

import httpx

from config import NaverConfig
from core.enums import Platforms
from crawler.scrapper import Scrapper, ScrapeResponse


class NaverScrapper(Scrapper):
    url = 'https://openapi.naver.com/v1/search/news.json?query="{subject}"&display=20&sort=date'

    async def scrape(self, subject: str, date: datetime) -> ScrapeResponse:
        format_url = self.url.format(subject=subject)
        header = {
            "X-Naver-Client-Id": NaverConfig.CLIENT_ID,
            "X-Naver-Client-Secret": NaverConfig.SECRET_KEY
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(format_url, headers=header)

        return ScrapeResponse(
            response=response,
            is_xml=False,
            is_json=True,
            platform=Platforms.Naver,
            keyword=subject
        )
