from typing import Union, List, Dict

from bs4 import BeautifulSoup

from datetime import datetime, timedelta

from core.enums import Platforms
from core.util import kst_now, parse_datetime_kst, is_outdated_kst, get_og_image
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

            # og:image 추출 및 S3 업로드
            image_url = get_og_image(link)

            self.append_to_list(
                parse_list=parsed_list,
                title=title,
                link=link,
                publisher=publisher,
                published_at=published_at,
                platform=Platforms.Daum,
                image_url=image_url,
                preview_content=None
            )

    def parse_li_list(self, li_list, parsed_list):
        for i in li_list:
            title_div = i.select_one('div.c-tit-doc')

            if not title_div:
                continue

            publisher = title_div.select_one('span.txt_info').text

            body_div = i.select_one('div.c-item-content')
            item_bundle = body_div.select_one('div.item-bundle-mid')

            published_at = self._convert_daum_datetime(
                item_bundle.select_one('span.txt_info').text
            )

            if is_outdated_kst(published_at, 1):
                continue

            image_url = body_div.select_one('img')
            if image_url:
                image_url = image_url["data-original-src"]
            else:
                # og:image 추출 및 S3 업로드
                link = item_bundle.find('a')["href"]
                image_url = get_og_image(link)

            preview_content = item_bundle.select_one('div.item-contents > p > a').text.strip()
            link = item_bundle.find('a')["href"]
            title = item_bundle.find('a').text.strip()

            self.append_to_list(
                parse_list=parsed_list,
                title=title,
                link=link,
                publisher=publisher,
                published_at=published_at,
                platform=Platforms.Daum,
                image_url=image_url,
                preview_content=preview_content
            )

    @staticmethod
    def _convert_daum_datetime(daum_date: str) -> datetime:
        if '시간전' in daum_date:
            hours_ago = int(daum_date.replace('시간전', ''))
            return kst_now() - timedelta(hours=hours_ago)

        elif '분전' in daum_date:
            minutes_ago = int(daum_date.replace('분전', ''))
            return kst_now() - timedelta(minutes=minutes_ago)

        else:
            return parse_datetime_kst(datetime.strptime(daum_date, '%Y.%m.%d'))
            # published_at = datetime.strptime(daum_date, '%Y.%m.%d')
