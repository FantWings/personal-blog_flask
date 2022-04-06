from flask import request
from . import userAPI
from utils.response import json_res
from crud.user import *


@userAPI.route("/userInfo", methods=["GET"])
def getUserInfo():
    """获取用户信息"""
    result = getFullInfo()
    return json_res(**result)

@userAPI.route("/avatar", methods=["GET"])
def getUserAvatar():
    """获取用户头像"""
    username = request.args.get("username")
    result = queryAvatar(username)
    return json_res(**result)
