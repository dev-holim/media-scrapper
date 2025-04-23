from typing import List
from dataclasses import dataclass

from core.enums import Platforms as PF
from crawler.parser import Data
from crawler.parser.bigkinds import BigKindsParser
from crawler.parser.daum import DaumParser
from crawler.parser.google import GoogleParser
from crawler.parser.naver import NaverParser
from crawler.scrapper import ScrapeResponse
from crawler.scrapper.bigkinds import BigKindsScrapper
from crawler.scrapper.daum import DaumScrapper
from crawler.scrapper.google import GoogleScrapper
from crawler.scrapper.naver import NaverScrapper
from database.model.keyword import Keyword
from database.repository.kerword import get_keywords
from util import kst_now

async def crawl():
    keyword_list = get_keywords()

    data_list = []
    for keyword in keyword_list:
        scrape_result = await scrape(keyword)
        if scrape_result:
            data_list.append({
                "keyword": keyword.keyword,
                "list": parse(scrape_result)
            })

    return data_list


async def scrape(keyword: Keyword):
    scrapper_map = {
        PF.Google: GoogleScrapper,
        PF.BigKinds: BigKindsScrapper,
        PF.Naver: NaverScrapper,
        PF.Daum: DaumScrapper,
    }

    scrapper_cls = scrapper_map.get(keyword.crawler)
    if scrapper_cls:
        scrapper = scrapper_cls()
        return await scrapper.scrape(keyword.keyword, kst_now())


def parse(result: ScrapeResponse):
    parser_map = {
        PF.Google: GoogleParser,
        PF.BigKinds: BigKindsParser,
        PF.Naver: NaverParser,
        PF.Daum: DaumParser
    }

    parser_cls = parser_map.get(result.platform)
    if result.is_xml and not result.is_json:
        return parser_cls().parse(result.response.text)
    else:
        return parser_cls().parse(result.response.json())


# def filtering(banned_publisher_set, platform_data_list: List[Data]):
#     return [
#         platform_data
#         for platform_data in platform_data_list
#         if platform_data.publisher not in banned_publisher_set
#     ]
