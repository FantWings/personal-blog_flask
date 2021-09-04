from . import db
from sqlalchemy.sql import func


class t_tag(db.Model):
    __tablename__ = "t_tag"
    id = db.Column(db.Integer, primary_key=True, comment="标签号")
    name = db.Column(db.String(64), nullable=False, unique=True, comment="名称")
    # ref_count = db.Column(db.Integer, nullable=False, default=1, comment="引用次数")
