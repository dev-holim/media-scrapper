from datetime import datetime
from typing import Union, List

from crawler.parser import Parser, Data
from core.util import cron_log, parse_datetime_kst, is_outdated_kst, get_og_image
from core.enums import Platforms


class BigKindsParser(Parser):

    def parse(self, json: Union[str, dict]) -> List[Data]:
        result_list = []
        for i in json.get("resultList"):
            kst_published_at = parse_datetime_kst(datetime.strptime(i['DATE'], '%Y%m%d'))

            if is_outdated_kst(kst_published_at, 1):
                continue
            else:
                cron_log(f'Google Scrap Success: {i["TITLE"]}')

            image_url = i["IMAGES"] + ".jpg" if i.get('IMAGES') else None
            if not image_url:
                image_url = get_og_image(i["PROVIDER_LINK_PAGE"])

            data = Data(
                title=i['TITLE'],
                link=i["PROVIDER_LINK_PAGE"],
                publisher=i['PROVIDER'],
                published_at=kst_published_at,
                image_url=image_url,
                preview_content=i["CONTENT"],
                platform=Platforms.BigKinds
            )
            result_list.append(data)

        return result_list
