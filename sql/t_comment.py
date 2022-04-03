from . import db
from sqlalchemy.sql import func
from . import t_archive
from . import t_user


class t_comment(db.Model):
    __tablename__ = "t_comment"
    id = db.Column(db.Integer, primary_key=True, comment="文档号")
    arch_id = db.Column(
        db.Integer,
        db.ForeignKey("t_archive.id"),
        nullable=False,
        comment="文章ID",
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey("t_user.id"), nullable=False, comment="评论所属用户ID"
    )
    comment = db.Column(db.Text, nullable=False, comment="评论内容")
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
    arch = db.relationship("t_archive", backref="comments_belong_to")
    user = db.relationship("t_user", backref="user_of_comments")
