from sqlalchemy import (Column, Integer, String)
from . import Model


class t_tag(Model):
    __tablename__ = "t_tag"
    id = Column(Integer, primary_key=True, comment="标签号")
    name = Column(String(64), nullable=False, unique=True, comment="名称")
    # ref_count = Column(Integer, nullable=False, default=1, comment="引用次数")
