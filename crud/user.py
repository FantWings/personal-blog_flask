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
        "email": query.email,
        "phone": query.phone,
        "qq": query.qq,
    }
    return {"data": data}
