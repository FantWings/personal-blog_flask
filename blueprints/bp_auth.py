from flask import Blueprint, request, make_response
from . import authAPI

from utils.response import json_res
from crud.users import registerNewAccount, sendCodeByEmail

print('[INFO] Blueprint - authAPI Loaded.')


@authAPI.route('/register', methods=['POST'])
def register():
    submit = request.get_json()
    username = submit.get('username')
    passwd = submit.get('passwd')
    registerNewAccount(username, passwd)
    return make_response(json_res(msg="注册成功"), 200)


@auth.route('/sendVerfiyCode', methods=['GET'])
def sendVerfiyCode():
    token = request.headers.get('token', default=0)
    method = request.args.get('method')
    
    if method = 'phone':
        return make_response(json_res(msg="方法暂未开放",status=1),200)
    if method = 'email':
        email = request.args.get('value')
        FcStatus = sendCodeByEmail(token,email)
        if FcStatus != 0 :
            return make_response(json_res(msg=FcStatus,status=1),200)
        return make_response(json_res(msg="邮件发送成功"),200)


# @authAPI.route('/login', methods=['POST'])
# def login():
#     """

#     """
