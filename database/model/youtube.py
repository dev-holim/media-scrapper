from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.sql import func

from database.model import BaseModel


class Youtube(BaseModel):
    __tablename__ = 'tb_youtube'

    title = Column(String, index=True)
    author = Column(String, nullable=False)
    url_path = Column(String, index=True)
    share_path = Column(String, index=True)
    image_path = Column(String, index=True)
    youtube_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_main = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)