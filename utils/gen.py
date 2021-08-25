import uuid
from random import Random, sample


def genToken(length):
    """
    token生成
    """
    token = ""
    chars = "0123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNOPQRSTUVWXYZ-_"
    temp = len(chars) - 1
    for i in range(length):
        token += chars[Random().randint(0, temp)]
    return token


def genUuid():
    """
    uuid生成
    """
    return uuid.uuid1().hex


def genMd5Password(password):
    """
    MD5生成
    """
    from hashlib import md5

    salted = "%sandgoodstuff" % (password)
    return md5(salted.encode("utf-8")).hexdigest()


def genRandomCode(lenguth):
    """
    验证码生成
    """
    code_list = []
    for i in range(10):  # 0~9
        code_list.append(str(i))
    for i in range(65, 91):  # A-Z
        code_list.append(chr(i))
    for i in range(97, 123):  # a-z
        code_list.append(chr(i))
    code = sample(code_list, lenguth)  # 随机取指定位数
    code_num = "".join(code)
    return code_num
