from . import db
from sqlalchemy.sql import func
from utils.gen import genUuid


class t_user(db.Model):
    __tablename__ = "t_user"
    id = db.Column(db.Integer, primary_key=True, nullable=False, comment='索引')
    username = db.Column(db.String(12), nullable=False, comment='用户名')
    uuid = db.Column(db.String(64),
                     nullable=False,
                     default=genUuid(),
                     comment='用户UUID')
    avatar = db.Column(db.String(64), comment='头像')
    password = db.Column(db.String(32), comment='密码')
    email = db.Column(db.String(32), nullable=False, comment='邮箱', unique=True)
    phone = db.Column(
        db.String(11),
        # 手机号验证功能没做完，暂时注释必填字段
        # nullable=False,
        comment='手机号',
        unique=True)
    qq = db.Column(db.String(13), comment='QQ号')
    create_time = db.Column(db.DateTime,
                            nullable=False,
                            server_default=func.now(),
                            comment='创建时间')
    update_time = db.Column(db.DateTime,
                            nullable=False,
                            server_default=func.now(),
                            comment='修改时间',
                            onupdate=func.now())
    vaild = db.Column(db.Boolean,
                      nullable=False,
                      default=False,
                      comment='账户状态')
