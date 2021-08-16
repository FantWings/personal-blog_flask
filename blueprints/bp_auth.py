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
    passwd = submit.get("passwd")
    log("Register request, user:{}, password:{}".format(username, passwd), "debug")
    result = registerNewAccount(username, passwd)
    return json_res(**result)


@authAPI.route("/sendVerfiyCode", methods=["GET"])
def sendVerfiyCode():
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


@authAPI.route("/verifyAccount", methods=["POST"])
def verifyAccount():
    token = request.headers.get("token", default=0)
    method = request.args.get("method")
    body = request.get_json()

    if method == "sms":
        return json_res(msg="方法暂未开放", status=1)
    if method == "email":
        result = activeAccount(token, body.verifyCode)
        return json_res(**result)
    else:
        return json_res(msg="接口参数错误！", status=1)


@authAPI.route("/login", methods=["POST"])
def login():
    body = request.get_json()
    result = userLogin(body.username, body.password)
    return json_res(**result)
