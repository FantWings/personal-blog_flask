from . import db
from sqlalchemy.sql import func


class Comments(db.Model):
    __tablename__ = "comments"
    id = db.Column(Integer, primary_key=True, comment='文档号')
    arch_id = db.Column(db.Integer,
                        nullable=False,
                        comment='文章ID',
                        ForeignKey("archives.id"))
    comment = db.Column(db.String(64), nullable=False, comment='评论')
    create_time = db.Column(db.DateTime,
                            nullable=False,
                            default=func.now(),
                            comment='创建时间')
    update_time = db.Column(db.DateTime,
                            nullable=False,
                            server_default=func.now(),
                            comment='修改时间',
                            onupdate=func.now())
    arch = relationship("Archives", backref="ref_comments")