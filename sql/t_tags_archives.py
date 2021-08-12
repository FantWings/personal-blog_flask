from . import db
from sqlalchemy.sql import func


class t_tags_archives(db.Model):
    __tablename__ = "t_tags_archvies"
    id = db.Column(db.Integer, primary_key=True, comment='映射号')
    tag_id = db.Column(
        db.Integer,
        db.ForeignKey("t_tags.id"),
        nullable=False,
        comment='标签ID',
    )
    arch_id = db.Column(
        db.Integer,
        db.ForeignKey("t_archvies.id"),
        nullable=False,
        comment='文章ID',
    )
    tag = db.relationship("t_tags", backref="ref_tags")
    arch = db.relationship("t_archives", backref="ref_archs")
