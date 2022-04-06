from os import path, urandom, getenv
from utils.log import log

log(
    """
********************************************************
                    ！ ！WARNING ！ ！
********************************************************
YOU ARE IN DEBUG MODE！
debugmode only for dev or debugging, not for producting.
importent config or infomation will be stdn out.
(sql, password, userinfo , or your top secret etc.)
DO NOT USE DEBUG MODE IN PRODUCTION ENV!
if you do this, used your own RISK!
""",
    "warn",
)


class FlaskConfig(object):
    """FLASK配置"""

    SECRET_KEY = urandom(24)

    """ SMTP配置 """
    SMTP_USER = getenv("SMTP_USER", "noreply@yourdomain.com")
    SMTP_PASS = getenv("SMTP_PASS", "SUPERPASSWD")
    SMTP_HOST = getenv("SMTP_HOST", "smtp.example.com")
    SMTP_PORT = getenv("SMTP_PORT", "465")

    """数据库配置"""
    if getenv("SQL_ENGINE", "sqlite") == "mysql":
        # 拼接SQL URI
        database_uri = "mysql://%s:%s@%s:%s/%s" % (
            getenv("SQL_USER", "root"),
            getenv("SQL_PASS", ""),
            getenv("SQL_HOST", "127.0.0.1"),
            getenv("SQL_PORT", "3306"),
            getenv("SQL_BASE", "BaseName"),
        )
        log("Using MySQL for SQL Engine.", "info")
    else:
        database_uri = False
        log("Using SQLite for SQL Engine.", "info")

    # 数据库路径
    base_dir = path.abspath(path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = database_uri or "sqlite:///" + path.join(
        base_dir, "sqlite.db"
    )
    log("SQL_URI is: {}".format(SQLALCHEMY_DATABASE_URI), "debug")

    # sqlalchemy配置
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    JSON_AS_ASCII = False

    """Redis配置"""
    REDIS_HOST = getenv("REDIS_HOST", "127.0.0.1")
    REDIS_PORT = getenv("REDIS_PORT", "6379")
    REDIS_DB = getenv("REDIS_DB", "0")
    REDIS_SESSION_TIMELIFE = getenv(int("REDIS_SESSION_TIMELIFE"), 172800)
