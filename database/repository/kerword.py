from typing import List

from database import session_scope
from database.model.keyword import Keyword


def get_keywords() -> List[Keyword]:
    with session_scope() as session:
        keyword_list = session.query(Keyword).filter(
            Keyword.is_active == True
        ).all()

        return keyword_list
