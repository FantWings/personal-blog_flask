from flask import request
from . import userAPI
from utils.response import json_res
from crud.user import *


@userAPI.route("/userInfo", methods=["GET"])
def getUserInfo():
    """获取用户信息"""
    token = request.headers.get("token")
    result = queryUser(token)
    return json_res(**result)


# @userAPI.route("/getRole", methods=["GET"])
# def getRoleInfo():
#     """获取用户权限"""
#     token = request.headers.get("token")
#     result = queryRole(token)
#     return json_res(**result)


@userAPI.route("/avatar", methods=["GET"])
def getUserAvatar():
    """获取用户头像"""
    username = request.args.get("username")
    result = queryAvatar(username)
    return json_res(**result)
