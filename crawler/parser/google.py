from datetime import datetime, timedelta
from typing import Union, Dict, List

from bs4 import BeautifulSoup

from crawler.parser import Parser, Data
from util import kst_now


class GoogleParser(Parser):

    def parse(self, xml: Union[str, dict]) -> List[Dict]:
        article_list = []
        soup = BeautifulSoup(xml, 'xml')

        for i in soup.select('channel > item'):
            try:
                item_soup = BeautifulSoup(i.prettify(formatter=None), 'xml')

                link = item_soup.find('link').text
                published_at = item_soup.find('pubDate').text
                description = item_soup.find('description')

                if description:
                    title = description.find('a').text
                    publisher = description.find('font').text

                    self.append_to_list(article_list, title, link, publisher, published_at)
            except:
                continue

        return article_list

    @staticmethod
    def append_to_list(
            article_list: list,
            title: str,
            link: str,
            publisher: str,
            published_at: str,
            platform: str = 'GOOGLE',
            image_url: str = None,
            preview_content: str = None
    ):
        link = link.strip()
        title = title.strip()
        publisher = publisher.strip()
        published_at = datetime.strptime(published_at.strip(), '%a, %d %b %Y %H:%M:%S GMT')

        if published_at + timedelta(hours=9) < kst_now() - timedelta(hours=1):
            return

        article_list.append(
            Data(
                title=title,
                link=link.strip(),
                publisher=publisher.strip(),
                published_at=published_at + timedelta(hours=9),
                image_url=None,
                preview_content=None,
                platform=platform
            )
        )
