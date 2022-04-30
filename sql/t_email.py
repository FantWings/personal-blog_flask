from sqlalchemy import (Column, Integer, String, DateTime)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from . import Model


class t_email(Model):
    __tablename__ = "t_email"
    email = Column(String(32), primary_key=True, nullable=False, comment="邮箱")
    verifyed = Column(Integer, nullable=False, default=0, comment="邮箱已验证")
    create_time = Column(DateTime,
                         nullable=False,
                         server_default=func.now(),
                         comment="创建时间")
    update_time = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        comment="修改时间",
        onupdate=func.now(),
    )
    owner = relationship("t_user", backref="email")
