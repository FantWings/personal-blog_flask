from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from . import Model


class t_archive_tag_map(Model):
    __tablename__ = "t_archive_tag_map"
    id = Column(Integer, primary_key=True, comment="映射号")
    tag_id = Column(
        Integer,
        ForeignKey("t_tag.id"),
        nullable=False,
        comment="标签ID",
    )
    arch_id = Column(
        Integer,
        ForeignKey("t_archive.id"),
        nullable=False,
        comment="关联的文章ID",
    )
    tag = relationship("t_tag", backref="ref_tag")
    arch = relationship("t_archive", backref="ref_arch")
