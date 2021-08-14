import random
from flask import current_app
from sql import db
from sql.t_user import t_user
from utils.redis import Redis
from utils.smtp import sendmail


def md5(password):
    """
    MD5生成
    """
    from hashlib import md5
    salted = "%sandgoodstuff" % (password)
    return md5(salted.encode("utf-8")).hexdigest()


def genRandomCode(lenguth):
    code_list = []
    for i in range(10):  # 0~9
        code_list.append(str(i))
    for i in range(65, 91):  # A-Z
        code_list.append(chr(i))
    for i in range(97, 123):  # a-z
        code_list.append(chr(i))
    code = random.sample(code_list, lenguth)  #随机取6位数
    code_num = "".join(code)
    return code_num


def getUserId(token):
    """
    获取用户ID
    """
    userId = Redis.read("session_{}".format(token))
    return userId


def registerNewAccount(username, passwd):
    """
    注册一个新账户
    """
    isUserExist = t_user.query.filter_by(username=username).first()
    if isUserExist:
        return {"status": 1, "msg": "账户已存在"}
    query = t_user(password=md5(passwd), email=username)
    db.session.add(query)
    db.session.commit()
    return 0


def sendCodeByEmail(token, email):
    uid = Redis.read("session_{}".format(token))
    query = t_user.query.filter_by(id=uid).first()
    if query is None:
        return {"status": 1, "msg": "UID无效！"}
    verifyCode = genRandomCode(lenguth=6)
    Redis.write("verify_{}".format(uid), verifyCode, expire=300)
    sendmail(
        """
        您的本次注册验证码为：
        {0}
        """.format(verifyCode), email, "账户注册",
        current_app.config.get("SITE_NAME"))
    return {"msg": "账户已成功注册"}


def activeAccount(token, verifyCode):
    uid = Redis.read("session_{}".format(token))
    if verifyCode != Redis.read("verify_{}".format(uid)):
        return {"status": 1, "msg": "验证码不正确"}

    query = t_user.query.filter_by(id=uid).first()
    if query is None:
        return {"status": 1, "msg": "参数有误！"}
    query.vaild = True
    db.session.commit()
    Redis.delete("verify_{}".format(uid))
    return {"msg": "账户已激活"}