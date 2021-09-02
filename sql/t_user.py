from . import db
from . import t_email
from sqlalchemy.sql import func


class t_user(db.Model):
    __tablename__ = "t_user"
    id = db.Column(db.Integer, primary_key=True, nullable=False, comment="索引")
    nickname = db.Column(db.String(16), nullable=False, comment="用户名")
    uuid = db.Column(db.String(64), nullable=False, comment="用户UUID")
    avatar = db.Column(db.String(256), comment="头像")
    password = db.Column(db.String(32), comment="密码")
    phone = db.Column(
        db.String(11),
        # 手机号验证功能没做完，暂时注释必填字段
        # nullable=False,
        comment="手机号",
        unique=True,
    )
    qq = db.Column(db.String(13), comment="QQ号")
    role = db.Column(db.Integer, nullable=False, default=0, comment="权限等级")
    deleted = db.Column(db.Integer, nullable=False, default=0, comment="注销标志")
    create_time = db.Column(
        db.DateTime, nullable=False, server_default=func.now(), comment="创建时间"
    )
    update_time = db.Column(
        db.DateTime,
        nullable=False,
        server_default=func.now(),
        comment="修改时间",
        onupdate=func.now(),
    )
    # 邮箱（外键）
    email_addr = db.Column(
        db.String(32), db.ForeignKey("t_email.email"), nullable=False, comment="邮箱"
    )
    email = db.relationship("t_email", backref="email_of_user")
