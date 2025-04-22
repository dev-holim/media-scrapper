from dataclasses import dataclass
from datetime import datetime
from typing import Union, Dict, List, Optional
from abc import ABC, abstractmethod


@dataclass
class Data:
    title: str
    publisher: str
    published_at: datetime
    link: str
    platform: str
    image_url: Optional[str]
    preview_content: Optional[str]


class Parser(ABC):

    @abstractmethod
    def parse(self, data: Union[str, dict]) -> List[Dict]:
        pass

    @staticmethod
    def append_to_list(
            parse_list: list,
            title: str, link: str,
            publisher: str, published_at: datetime,
            platform: str,
            image_url: str = None, preview_content: str = None
    ):
        parse_list.append(
            Data(
                title=title,
                link=link,
                publisher=publisher,
                published_at=published_at,
                image_url=image_url,
                preview_content=preview_content,
                platform=platform
            )
        )
