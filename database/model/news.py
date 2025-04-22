from sqlalchemy import Column, Date, Boolean, Text

from database.model import BaseModel

class News(BaseModel):
    __tablename__ = "tb_news"

    title = Column(Text, nullable=False)
    publisher = Column(Text, nullable=False)
    published_at = Column(Date, nullable=False)
    link = Column(Text, nullable=False)
    keyword = Column(Text, nullable=False)
    platform = Column(Text, nullable=False)
    image_url = Column(Text, nullable=True, default=None)
    is_active = Column(Boolean, nullable=False, default=False)