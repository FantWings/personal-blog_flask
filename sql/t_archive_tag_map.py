from . import db
from . import t_tag, t_archive


class t_archive_tag_map(db.Model):
    __tablename__ = "t_archive_tag_map"
    id = db.Column(db.Integer, primary_key=True, comment="映射号")
    tag_id = db.Column(
        db.Integer,
        db.ForeignKey("t_tag.id"),
        nullable=False,
        comment="标签ID",
    )
    arch_id = db.Column(
        db.Integer,
        db.ForeignKey("t_archive.id"),
        nullable=False,
        comment="关联的文章ID",
    )
    tag = db.relationship("t_tag", backref="ref_tag")
    arch = db.relationship("t_archive", backref="ref_arch")
