import os
from datetime import timedelta


class Config(object):
    # SQLALCHEMY配置
    SQLALCHEMY_DATABASE_URI = "mysql://{}:{}@{}:{}/{}".format(
        os.getenv('SQL_USER', 'root'), os.getenv('SQL_PASS', None),
        os.getenv('SQL_HOST', '127.0.0.1'), os.getenv('SQL_PORT', 3306),
        os.getenv('SQL_BASE', 'blog'))

    print('[INFO] SQL_URI is: {}'.format(SQLALCHEMY_DATABASE_URI))

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 禁用ASCII编码
    JSON_AS_ASCII = False

    # 设置SESSION安全密钥
    SECRET_KEY = os.urandom(24)

    # 设置SESSION有效期
    PERMANENT_SESSION_LIFETIME = timedelta(days=31)

    # 开启SQLALCHEMY哆嗦模式
    SQLALCHEMY_ECHO = os.getenv('SQL_ECHO', False)
