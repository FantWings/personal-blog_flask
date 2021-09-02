from flask import request
from . import authAPI
from utils.log import log

from utils.response import json_res
from crud.auth import *

log("Loaded AuthAPI. [Ver 1.2]")


@authAPI.route("/register", methods=["POST"])
def register():
    submit = request.get_json()
    username = submit.get("username")
    password = submit.get("password")
    email = submit.get("email")
    log("Register request, user:{}, password:{}".format(username, password), "debug")
    result = registerNewAccount(username, password, email)
    return json_res(**result)


@authAPI.route("/2fa/sendVerifyCode", methods=["GET"])
def sendVerifyCode():
    token = request.headers.get("token", default=0)
    method = request.args.get("method")

    if method == "sms":
        return json_res(msg="方法暂未开放", status=1)
    if method == "email":
        email = request.args.get("value")
        result = sendCodeByEmail(token, email)
        return json_res(**result)
    else:
        return json_res(msg="接口参数错误！", status=1)


@authAPI.route("/2fa/bound", methods=["POST"])
def bound2fa():
    token = request.headers.get("token", default=0)
    method = request.args.get("method")
    body = request.get_json()

    if method == "sms":
        return json_res(msg="方法暂未开放", status=1)
    if method == "email":
        result = add2FAToAccount(token, body["verifyCode"])
        return json_res(**result)
    else:
        return json_res(msg="接口参数错误！", status=1)


@authAPI.route("/login", methods=["POST"])
def login():
    body = request.get_json()
    result = userLogin(body["username"], body["password"])
    return json_res(**result)


@authAPI.route("/logout", methods=["GET"])
def logout():
    token = request.headers.get("token")
    result = logoutUser(token)
    return json_res(**result)
