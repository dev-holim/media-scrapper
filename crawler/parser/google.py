from typing import Union, Dict, List

from bs4 import BeautifulSoup

from core.enums import Platforms
from crawler.parser import Parser, Data
from core.util import parse_datetime_kst, is_outdated_kst, cron_log


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
            except Exception as e:
                cron_log(e)
                continue

        return article_list

    @staticmethod
    def append_to_list(
            article_list: list,
            title: str,
            link: str,
            publisher: str,
            published_at: str,
            platform: Platforms = Platforms.Google,
            image_url: str = None,
            preview_content: str = None
    ):
        link = link.strip()
        title = title.strip()
        publisher = publisher.strip()
        # published_at = datetime.strptime(published_at.strip(), '%a, %d %b %Y %H:%M:%S GMT')

        # 1시간 이내의 뉴스만 저장
        kst_published_at = parse_datetime_kst(published_at.strip(), is_gmt=True)
        if is_outdated_kst(kst_published_at, 1):
            return
        else:
            cron_log(f'Google Scrap Success: {title}')

        article_list.append(
            Data(
                title=title,
                link=link,
                publisher=publisher,
                published_at=kst_published_at,
                image_url=None,
                preview_content=None,
                platform=platform
            )
        )
