from core.util import cron_log, parse_datetime_kst, is_outdated_kst, get_og_image
from crawler.parser import Parser, Data
from core.enums import Platforms


class NaverParser(Parser):

    def parse(self, data: dict):
        parse_list = []

        for item in data['items']:
            title = self.replace(item['title'], ('<b>', '</b>', '&quot'), ("", "", ""))
            # published_at = datetime.strptime(item["pubDate"][:-6], "%a, %d %b %Y %H:%M:%S")

            kst_published_at = parse_datetime_kst(item["pubDate"][:-6])

            if is_outdated_kst(kst_published_at, 1):
                continue
            else:
                cron_log(f'Naver Scrap Success: {title}')

            try:
                publisher = item['originallink'].split('//')[1].split('/')[0]
            except IndexError:
                publisher = '본문 참고'

            # og:image 추출 및 S3 업로드
            image_url = get_og_image(item['originallink'])

            parse_list.append(
                Data(
                    title=title,
                    link=item['originallink'],
                    publisher=publisher,
                    published_at=kst_published_at,
                    image_url=image_url,
                    platform=Platforms.Naver,
                    preview_content=item['description']
                )
            )

        return parse_list

    @staticmethod
    def replace(string: str, target_list, replace_list):
        for ind, target in enumerate(target_list):
            string = string.replace(target, replace_list[ind])

        return string
