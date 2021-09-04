from . import db
from . import t_user
from sqlalchemy.sql import func


class t_archive(db.Model):
    __tablename__ = "t_archive"
    id = db.Column(db.Integer, primary_key=True, comment="文档号")
    title = db.Column(db.String(64), nullable=False, comment="标题")
    content = db.Column(db.Text, nullable=False, comment="正文")
    views = db.Column(db.Integer, nullable=False, default=0, comment="阅读数")
    cover_image = db.Column(db.String(32), nullable=True, comment="封面图")
    time_for_read = db.Column(
        db.SmallInteger, nullable=False, default=5, comment="所需阅读时间"
    )
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

    author_id = db.Column(
        db.Integer, db.ForeignKey("t_user.id"), nullable=False, comment="作者"
    )
    author = db.relationship("t_user", backref="author_of_archive")
