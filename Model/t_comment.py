from sqlalchemy import (Column, Integer, Text, DateTime, ForeignKey)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from . import Model


class t_comment(Model):
    __tablename__ = "t_comment"
    id = Column(Integer, primary_key=True, comment="文档号")
    arch_id = Column(
        Integer,
        ForeignKey("t_archive.id"),
        nullable=False,
        comment="文章ID",
    )
    user_id = Column(Integer,
                     ForeignKey("t_user.id"),
                     nullable=False,
                     comment="评论所属用户ID")
    comment = Column(Text, nullable=False, comment="评论内容")
    create_time = Column(DateTime,
                         nullable=False,
                         default=func.now(),
                         comment="创建时间")
    update_time = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        comment="修改时间",
        onupdate=func.now(),
    )
    arch = relationship("t_archive", backref="comments_belong")
    user = relationship("t_user", backref="comments_owner")
