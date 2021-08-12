from sql import db
from sql.t_user import t_user


def md5(password):
    """
    MD5生成
    """
    from hashlib import md5
    salted = '%sandgoodstuff' % (password)
    return md5(salted.encode('utf-8')).hexdigest()


def genCode():
    code_list = []
    for i in range(10):  # 0~9
        code_list.append(str(i))
    for i in range(65, 91):  # A-Z
        code_list.append(chr(i))
    for i in range(97, 123):  # a-z
        code_list.append(chr(i))
    code = random.sample(code_list, 6)  #随机取6位数
    code_num = ''.join(code)
    return code_num


def getUserId(token):
    """
    获取用户ID
    """
    userId = Redis.read('session_{}'.format(token))
    return userId


def registerNewAccount(username, passwd):
    """
    注册一个新账户
    """
    isUserExist = t_user.query.filter_by(username=username).first()
    if isUserExist:
        return response(msg='账户已存在！', status=1)
    query = t_user(password=md5(passwd), email=email)
    db.session.add()
    db.session.commit()


def sendCodeByEmail(token, email):
    uid = Redis.read('session_{}'.format(token))
    query = t_user.query.with_entities(t_user.username).filter_by(uid).first()
    if query is None:
        return 'UID无效！'
    verifyCode = genCode()
    Redis.write('verify_{}'.format(query.username), verifyCode, expire=300)
    sendmail(
        '''
        您的本次注册验证码为：
        {0}
        '''.format(verifyCode), email, '账户注册',
        current_app.config.get('SITE_NAME'))
    return 0