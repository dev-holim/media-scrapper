from sqlalchemy import Column, Integer, Text, Boolean, Enum

from core.enums import Platforms
from database.model import BaseModel


class Keyword(BaseModel):
    __tablename__ = 'tb_keyword'

    keyword = Column(Text, nullable=False)
    crawler = Column(Enum(Platforms), nullable=False)
    is_active = Column(Boolean, nullable=False, default=False)
