from datetime import datetime
import httpx
from json import dumps

from core.enums import Platforms
from crawler.scrapper import Scrapper, ScrapeResponse


class BigKindsScrapper(Scrapper):
    subject_key = "searchKey"
    start_date_key = "startDate"
    end_date_key = "endDate"

    url = "https://www.bigkinds.or.kr/api/news/search.do"

    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        # 'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
        'Aceept': 'application/json, text/javascript, */*; q=0.01', 'Accept-Encoding': 'gzip, deflate, br',
        'Origin': 'https://www.bigkinds.or.kr',
        'Referer': 'https://www.bigkinds.or.kr/v2/news/search.do'
    }

    payload = {
        "byLine": "",
        "categoryCodes": [],
        "dateCodes": [],
        "editorialIs": False,
        "incidentCodes": [],
        "indexName": "news",
        "isNotTmUsable": False,
        "isTmUsable": False,
        "mainTodayPersonYn": "",
        "networkNodeType": "",
        "newIds": [],
        "providerCodes": [],
        "resultNumber": 10,
        "searchFilterType": "1",
        subject_key: "텔레픽스",
        "searchKeys": [{}],
        "searchScopeType": "1",
        "searchSortType": "date",
        "sortMethod": "date",
        start_date_key: "2023-08-13",
        end_date_key: "2023-11-16",
        "startNo": 1,
        "topicOrigin": ""
    }

    def _set_keyword(self, subject):
        self.payload[self.subject_key] = subject

    def _set_date(self, date: datetime):
        str_date = date.strftime("%Y-%m-%d")

        self.payload[self.start_date_key] = str_date
        self.payload[self.end_date_key] = str_date

    async def scrape(self, subject: str, date: datetime) -> ScrapeResponse:
        self._set_keyword(subject)
        self._set_date(date)

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=BigKindsScrapper.url,
                headers=BigKindsScrapper.headers,
                json=self.payload
            )

        return ScrapeResponse(
            response=response,
            is_xml=False,
            is_json=True,
            platform=Platforms.BigKinds,
            keyword=subject
        )
