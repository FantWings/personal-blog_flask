from flask import request
from . import userAPI
from utils.log import log
from utils.response import json_res
from crud.user import *


@userAPI.route("/userInfo", methods=["GET"])
def getUserInfo():
    """获取用户信息"""
    token = request.headers.get("token")
    result = queryUser(token)
    print(result)
    return json_res(**result)
