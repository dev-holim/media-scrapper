from datetime import datetime, timedelta
from typing import Union, List, Dict

from crawler.parser import Parser, Data
from util import kst_now


class BigKindsParser(Parser):

    def parse(self, json: Union[str, dict]) -> List[Dict]:
        result_list = []

        for i in json['resultList']:
            p_a = datetime.strptime(i['DATE'], '%Y%m%d')

            if p_a < kst_now() - timedelta(hours=1):
                continue

            data = Data(
                title=i['TITLE'],
                link=i["PROVIDER_LINK_PAGE"],
                publisher=i['PROVIDER'],
                published_at=p_a,
                image_url=i["IMAGES"] + ".jpg" if i.get('IMAGES') else None,
                preview_content=i["CONTENT"],
                platform='BIGKINDS'
            )
            result_list.append(data)

        return result_list
