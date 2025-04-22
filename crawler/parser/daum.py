from typing import Union, List, Dict

from bs4 import BeautifulSoup

from datetime import datetime, timedelta

from util import kst_now
from crawler.parser import Parser


class DaumParser(Parser):

    def parse(self, data: Union[str, dict]) -> List[Dict]:
        parsed_list = []
        soup = BeautifulSoup(data, 'lxml')

        news_list = soup.select_one('.list_news')
        li_list = soup.select('ul.c-list-basic > li')

        if news_list is not None:
            self.parse_news_list(news_list, parsed_list)

        elif li_list is not None:
            self.parse_li_list(li_list, parsed_list)

        return parsed_list

    def parse_news_list(self, news_list, parsed_list):
        for i in news_list.select('.wrap_cont'):
            article_a_tag = i.select_one('a.tit_main')
            publisher_a_tag = i.select_one('a.f_nb')
            published_at = i.select_one('span.f_nb').text

            title = article_a_tag.text
            link = article_a_tag['href']
            publisher = publisher_a_tag.text
            published_at = self._convert_daum_datetime(published_at)

            self.append_to_list(
                parse_list=parsed_list,
                title=title,
                link=link,
                publisher=publisher,
                published_at=published_at,
                platform='DAUM',
                image_url=None,
                preview_content=None
            )

    def parse_li_list(self, li_list, parsed_list):
        for i in li_list:
            title_div = i.select_one('div.c-tit-doc')
            publisher = title_div.select_one('span.txt_info').text

            body_div = i.select_one('div.c-item-content')
            item_bundle = body_div.select_one('div.item-bundle-mid')

            published_at = self._convert_daum_datetime(
                item_bundle.select_one('span.txt_info').text
            )

            if published_at < kst_now() - timedelta(hours=1):
                continue

            image_url = body_div.select_one('img')
            if image_url:
                image_url = image_url["data-original-src"]

            preview_content = item_bundle.select_one('div.item-contents > p > a').text.strip()
            link = item_bundle.find('a')["href"]
            title = item_bundle.find('a').text.strip()

            self.append_to_list(
                parse_list=parsed_list,
                title=title,
                link=link,
                publisher=publisher,
                published_at=published_at,
                platform='DAUM',
                image_url=image_url,
                preview_content=preview_content
            )

    @staticmethod
    def _convert_daum_datetime(daum_date: str) -> datetime:

        if '시간전' in daum_date:
            hours_ago = int(daum_date.replace('시간전', ''))
            published_at = kst_now() - timedelta(hours=hours_ago)

        elif '분전' in daum_date:
            minutes_ago = int(daum_date.replace('분전', ''))
            published_at = kst_now() - timedelta(minutes=minutes_ago)

        else:
            published_at = datetime.strptime(daum_date, '%Y.%m.%d')

        return published_at
