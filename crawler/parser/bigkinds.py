from datetime import datetime, timedelta
from typing import Union, List, Dict

from crawler.parser import Parser, Data
from util import cron_log, parse_datetime_kst, is_outdated_kst
from core.enums import Platforms


class BigKindsParser(Parser):

    def parse(self, json: Union[str, dict]) -> List[Data]:
        result_list = []
        for i in json.get("resultList"):
            kst_published_at = parse_datetime_kst(datetime.strptime(i['DATE'], '%Y%m%d'))

            if is_outdated_kst(kst_published_at, 24):
                continue
            else:
                cron_log(f'Google Scrap Success: {i["TITLE"]}')

            data = Data(
                title=i['TITLE'],
                link=i["PROVIDER_LINK_PAGE"],
                publisher=i['PROVIDER'],
                published_at=kst_published_at,
                image_url=i["IMAGES"] + ".jpg" if i.get('IMAGES') else None,
                preview_content=i["CONTENT"],
                platform=Platforms.BigKinds
            )
            result_list.append(data)

        return result_list
