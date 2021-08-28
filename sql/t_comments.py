from . import db
from sqlalchemy.sql import func
from . import t_archives
from . import t_user


class t_comments(db.Model):
    __tablename__ = "t_comments"
    id = db.Column(db.Integer, primary_key=True, comment="文档号")
    arch_id = db.Column(
        db.Integer,
        db.ForeignKey("t_archives.id"),
        nullable=False,
        comment="文章ID",
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey("t_user.id"), nullable=False, comment="评论所属用户ID"
    )
    comment = db.Column(db.String(64), nullable=False, comment="评论内容")
    create_time = db.Column(
        db.DateTime, nullable=False, default=func.now(), comment="创建时间"
    )
    update_time = db.Column(
        db.DateTime,
        nullable=False,
        server_default=func.now(),
        comment="修改时间",
        onupdate=func.now(),
    )
    arch = db.relationship("t_archives", backref="comments_belong_to")
    user = db.relationship("t_user", backref="user_of_comments")
