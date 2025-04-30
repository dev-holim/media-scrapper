from database import session_scope
from database.model.youtube import Youtube
from sqlalchemy.exc import IntegrityError


def insert_youtube(youtube: Youtube):
    with session_scope() as session:
        try:
            session.add(youtube)
            session.commit()

        except IntegrityError:
            print('EXIST', youtube.title)
            session.rollback()