from datetime import datetime
import httpx

from core.enums import Platforms
from crawler.scrapper import Scrapper, ScrapeResponse


class DaumScrapper(Scrapper):
    url = 'https://search.daum.net/search?w=news&nil_search=btn&DA=STC&enc=utf8&cluster=y&cluster_page=1&q="{subject}"&p=1&sort=accuracy'

    async def scrape(self, subject: str, date: datetime) -> ScrapeResponse:
        format_url = self.url.format(subject=subject)
        async with httpx.AsyncClient() as client:
            response = await client.get(format_url)

        return ScrapeResponse(
            response=response,
            is_xml=True,
            is_json=False,
            platform=Platforms.Daum,
            keyword=subject
        )
