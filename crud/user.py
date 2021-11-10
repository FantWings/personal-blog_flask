# from sql import db
from utils.log import log
from sql.t_user import t_user

# from utils.redis import Redis
from .auth import loginRequired


@loginRequired
def queryUser(uid):
    query = t_user.query.filter_by(id=uid).first()
    data = {
        "nickname": query.nickname,
        "uuid": query.uuid,
        "avatar": query.avatar,
        "email": {"addr": query.email.email, "verifyed": query.email.verifyed},
        "phone": query.phone,
        "qq": query.qq,
        "is_admin": query.is_admin,
    }
    log(
        "Returned user info: email:{email}, uuid:{uuid}, is_admin:{is_admin}".format(
            **data
        ),
        "debug",
    )
    return {"data": data}


@loginRequired
def queryRole(uid):
    query = t_user.query.with_entities(t_user.is_admin).filter_by(id=uid).first()
    return {"data": query.is_admin}


def queryAvatar(email):
    query = (
        t_user.query.with_entities(t_user.avatar, t_user.nickname)
        .filter_by(email_addr=email)
        .first()
    )
    if not query:
        return {"data": None}

    return {"data": {"avatar": query.avatar, "nickname": query.nickname}}
