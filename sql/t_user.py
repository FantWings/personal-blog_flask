from sqlalchemy import (Column, Integer, String, DateTime, ForeignKey)
from sqlalchemy.sql import func
# from sqlalchemy.orm import relationship
from . import Model


class t_user(Model):
    __tablename__ = "t_user"
    id = Column(Integer, primary_key=True, nullable=False, comment="索引")
    nickname = Column(String(16), nullable=False, comment="用户名")
    uuid = Column(String(64), nullable=False, comment="用户UUID")
    avatar = Column(String(256), comment="头像")
    password = Column(String(32), comment="密码")
    phone = Column(
        String(11),
        # 手机号验证功能没做完，暂时注释必填字段
        # nullable=False,
        comment="手机号",
        unique=True,
    )
    qq = Column(String(13), comment="QQ号")
    is_admin = Column(Integer, nullable=False, default=0, comment="权限等级")
    deleted = Column(Integer, nullable=False, default=0, comment="注销标志")
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
    # 邮箱（外键）
    email_addr = Column(String(32),
                        ForeignKey("t_email.email"),
                        nullable=False,
                        comment="邮箱")
