from flask_sqlalchemy import SQLAlchemy
from utils.log import log

log('SQLAlchemy Loaded.')

# 实例化SQL Alchemy
db = SQLAlchemy()