from flask import json, request
from . import authAPI

from utils.response import json_res
from crud.users import registerNewAccount, sendCodeByEmail, activeAccount

print('[INFO] Blueprint - authAPI Loaded.')


@authAPI.route('/register', methods=['POST'])
def register():
    submit = request.get_json()
    username = submit.get('username')
    passwd = submit.get('passwd')
    result = registerNewAccount(username, passwd)
    return json_res(**result)


@authAPI.route('/sendVerfiyCode', methods=['GET'])
def sendVerfiyCode():
    token = request.headers.get('token', default=0)
    method = request.args.get('method')

    if method is 'sms':
        return json_res(msg="方法暂未开放", status=1)
    if method is 'email':
        email = request.args.get('value')
        result = sendCodeByEmail(token, email)
        return json_res(**result)


@authAPI.route('/verifyAccount', method=['POST'])
def verifyAccount():
    token = request.headers.get('token', default=0)
    method = request.args.get('method')
    body = request.get_json()

    if method is 'sms':
        return json_res(msg="方法暂未开放", status=1)
    if method is 'email':
        result = activeAccount(token, body.verifyCode)
        return json_res(**result)


# @authAPI.route('/login', methods=['POST'])
# def login():
#     """

#     """
