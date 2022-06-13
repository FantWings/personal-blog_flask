from uuid import uuid1
from time import time
from flask import request, Blueprint
from sqlalchemy import or_
from Model import session as sql
from Model.t_user import t_user
from Model.t_email import t_email
from utils.response import json_response
from utils.sms import SMS
from utils.generator import gen_random_code,gen_md5_password,gen_token,gen_gravatar_url
from utils.redis import Redis

authAPI = Blueprint("auth", __name__, url_prefix="/auth")

@authAPI.route("/2fa/send_verify_code", methods=["GET"])
def send_verify_code():
    """发送短信验证码"""
    try:
        phone_num = request.args.get('phone_num')
        verify_code = gen_random_code(1,6)
        
        if Redis.read(f'{phone_num}/verify_code_vaild'):
            return json_response(status=1, msg="验证码尚未过期，请稍后再试")

        client = SMS("1400658044","1388522")
        client.send([phone_num],[verify_code,"5"])

        Redis.write(f'{phone_num}/verify_code',verify_code,300)
        Redis.write(f'{phone_num}/verify_code_vaild',verify_code,60)

        return json_response(status=0)
    except Exception as err:
        return json_response(msg=f"{err}", status=1)


@authAPI.route("/login", methods=["POST"])
def login_as_password():
    """用户登录"""
    body = request.get_json()
    username = body['username']
    password = body['password']
    smsLogin = body['smsLogin']
    
    # 检查参数
    if not username or not password:
        return json_response(status=1,msg="用户名和密码不可为空")

    # 检查是否为短信登录模式
    if smsLogin:
        if Redis.read(f"{username}/verify_code") != password:
            return json_response(status=1,msg="验证码有误，请核对")

    # 查询用户是否存在
    query = (sql.query(t_user)
            .with_entities(t_user.id, t_user.password)
            .filter(or_(t_user.username==username,t_user.phone==username))
            .first())
    if query is None:
        if not smsLogin:
            return json_response(status=1,msg="用户名或密码错误")
        # 写入用户名到数据库
        addUser = t_user(
            username=username,
            nickname=username,
            avatar=gen_gravatar_url('none@avatar.com'),
            uuid=uuid1().hex,
            phone=username,
        )
        sql.add(addUser)
        sql.commit()
        sql.flush()
        query = (sql.query(t_user)
            .with_entities(t_user.id)
            .filter(t_user.phone==username)
            .first())

    # 检查密码是否一致
    if not smsLogin:
        if gen_md5_password(password) != query.password:
            return json_response(status=1,msg="用户名或密码错误")

    token = gen_token(32)
    Redis.write(f"{token}/uid", query.id)
    return json_response({
            "token": token,
            "expTime": int(round(time() * 1000)) + 172800000
    })


@authAPI.route("/logout", methods=["GET"])
def user_logout():
    """用户登出"""
    token = request.headers.get("token")
    Redis.delete("session_{}".format(token))
    return json_response(status=0)
