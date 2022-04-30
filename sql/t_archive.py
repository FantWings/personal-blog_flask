from sqlalchemy import (Column, Integer, String, Text, DateTime, SmallInteger,
                        ForeignKey)
from sqlalchemy.sql import functions
from sqlalchemy.orm import relationship
from . import Model


class t_archive(Model):
    __tablename__ = "t_archive"
    id = Column(Integer, primary_key=True, comment="文档号")
    title = Column(String(64), nullable=False, comment="标题")
    content = Column(Text, nullable=False, comment="正文")
    views = Column(Integer, nullable=False, default=0, comment="阅读数")
    cover_image = Column(String(256), nullable=True, comment="封面图")
    time_for_read = Column(SmallInteger,
                           nullable=False,
                           default=5,
                           comment="所需阅读时间")
    create_time = Column(DateTime,
                         nullable=False,
                         default=functions.now(),
                         comment="创建时间")
    update_time = Column(
        DateTime,
        nullable=False,
        server_default=functions.now(),
        comment="修改时间",
        onupdate=functions.now(),
    )
    author_id = Column(Integer,
                       ForeignKey("t_user.id"),
                       nullable=False,
                       comment="作者")
    author = relationship("t_user", backref="belogs_to")
