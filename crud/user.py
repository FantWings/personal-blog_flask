# from sql import db
# from utils.log import log
from sql.t_user import t_user

# from utils.redis import Redis
from .auth import loginRequired

@loginRequired
# 查询用户数据
def getFullInfo(uid):
    target_user=t_user.query.filter_by(id=uid).first()
    data = {
    "nickname": target_user.nickname,
    "uuid": target_user.uuid,
    "avatar": target_user.avatar,
    "email": {"addr": target_user.email.email, "verifyed": target_user.email.verifyed},
    "phone": target_user.phone,
    "qq": target_user.qq,
    "is_admin": target_user.is_admin,
    }
    return {"data": data}

def queryAvatar(email):
    query = (
        t_user.query.with_entities(t_user.avatar, t_user.nickname)
        .filter_by(email_addr=email)
        .first()
    )
    if not query:
        return {"data": None}
    return {"data": {"avatar": query.avatar, "nickname": query.nickname}}
