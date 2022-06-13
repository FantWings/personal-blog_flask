from flask import request, Blueprint
from sqlalchemy import or_
from Model import session as sql
from functions.login_check import login_required
from utils.response import json_response
from Model.t_user import t_user

userAPI = Blueprint("user", __name__, url_prefix="/user")

@userAPI.route("/userInfo", methods=["GET"])
@login_required
def getUserInfo(uid):
    """获取用户信息"""
    target_user=t_user.query.filter_by(id=uid).first()
    data = {
        "nickname": target_user.nickname,
        "uuid": target_user.uuid,
        "avatar": target_user.avatar,
        "email": {
            "addr": target_user.email.email if target_user.email else None, 
            "verifyed": target_user.email.verifyed if target_user.email else None
            },
        "phone": target_user.phone,
        "qq": target_user.qq,
        "is_admin": target_user.is_admin,
    }
    return json_response(data)

@userAPI.route("/avatar", methods=["GET"])
def getUserAvatar():
    """获取用户头像和昵称"""
    username = request.args.get("username")
    query = (
        sql.query(t_user).with_entities(t_user.avatar, t_user.username)
        .filter(or_(t_user.username==username,t_user.phone==username))
        .first()
    )
    if not query:
        return {"data": None}
    return json_response({"avatar": query.avatar, "nickname": query.username})
