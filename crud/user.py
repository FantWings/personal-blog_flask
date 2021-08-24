# from sql import db
from sql.t_user import t_user

# from utils.redis import Redis
from .auth import loginRequired


@loginRequired
def queryUser(uid):
    query = t_user.query.filter_by(id=uid).first()
    data = {
        "username": query.username,
        "uuid": query.uuid,
        "avatar": query.avatar,
        "email": {"addr": query.email.email, "verifyed": query.email.verifyed},
        "phone": query.phone,
        "qq": query.qq,
        "role": query.role
    }
    return {"data": data}
