# from sql import db
# from utils.log import log
from sql.t_user import t_user

# from utils.redis import Redis
from .auth import loginRequired

@loginRequired
class User:
    def __init__(self,uid):
        self.target_user = t_user.query.filter_by(id=uid).first()
    
    # 查询用户数据
    def getFullInfo(self):
        data = {
        "nickname": self.target_user.nickname,
        "uuid": self.target_user.uuid,
        "avatar": self.target_user.avatar,
        "email": {"addr": self.target_user.email.email, "verifyed": self.target_user.email.verifyed},
        "phone": self.target_user.phone,
        "qq": self.target_user.qq,
        "is_admin": self.target_user.is_admin,
        }
        return {"data": data}

    def getRole(self):
        return {"data": self.target_user.is_admin}


def queryAvatar(email):
    query = (
        t_user.query.with_entities(t_user.avatar, t_user.nickname)
        .filter_by(email_addr=email)
        .first()
    )
    if not query:
        return {"data": None}
    return {"data": {"avatar": query.avatar, "nickname": query.nickname}}
