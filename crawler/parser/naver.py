from datetime import datetime, timedelta

from util import kst_now, cron_log
from crawler.parser import Parser, Data


class NaverParser(Parser):

    def parse(self, data: dict):
        parse_list = []

        for item in data['items']:
            title = self.replace(item['title'], ('<b>', '</b>', '&quot'), ("", "", ""))
            published_at = datetime.strptime(item["pubDate"][:-6], "%a, %d %b %Y %H:%M:%S")

            if published_at < kst_now() - timedelta(hours=60):
                continue
            else:
                cron_log(f'Naver Scrap Success: {title}')

            try:
                publisher = item['originallink'].split('//')[1].split('/')[0]
            except IndexError:
                publisher = '본문 참고'

            parse_list.append(
                Data(
                    title=title,
                    link=item['originallink'],
                    publisher=publisher,
                    published_at=published_at,
                    image_url=None,
                    platform='NAVER',
                    preview_content=item['description']
                )
            )

        return parse_list

    @staticmethod
    def replace(string: str, target_list, replace_list):
        for ind, target in enumerate(target_list):
            string = string.replace(target, replace_list[ind])

        return string
