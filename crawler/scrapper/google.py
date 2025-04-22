from datetime import datetime
import httpx

from core.enums import Platforms
from crawler.scrapper import Scrapper, ScrapeResponse


class GoogleScrapper(Scrapper):
    url = 'https://news.google.com/rss/search?q="{subject}"+when:1d&hl=ko&gl=KR&ceid=KR:ko'
    header = None
    payload = None

    async def scrape(self, subject: str, date: datetime) -> ScrapeResponse:
        format_url = self.url.format(subject=subject)
        async with httpx.AsyncClient() as client:
            response = await client.get(format_url)

        return ScrapeResponse(
            response=response,
            platform=Platforms.Google,
            is_json=False,
            is_xml=True,
            keyword=subject
        )
