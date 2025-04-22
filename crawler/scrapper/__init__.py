from datetime import datetime
from abc import ABC, abstractmethod
from dataclasses import dataclass
from httpx import Response

from core.enums import Platforms


@dataclass
class ScrapeResponse:
    response: Response
    platform: Platforms
    keyword: str
    is_xml: bool
    is_json: bool


class Scrapper(ABC):
    url: str
    header: dict
    payload: dict

    @abstractmethod
    async def scrape(self, subject: str, date: datetime) -> ScrapeResponse:
        pass
