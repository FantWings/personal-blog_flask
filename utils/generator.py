from random import Random, sample
from hashlib import md5


def gen_token(length: int = 32):
    """
    token生成(默认32位)
    """
    token = ""
    chars = "0123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNOPQRSTUVWXYZ-_"
    temp = len(chars) - 1
    for i in range(length):
        token += chars[Random().randint(0, temp)]
    return token


def gen_random_code(mode: int = 0,lenguth: int = 6):
    """
    验证码生成(默认6位)
    mode: 0 = 全部, 1 = 仅限数字, 2 = 英文+数字, 3 = 大小写英文+数字
    """
    code_list = []
    if mode >= 1 or 0 in mode:
        for i in range(10):  # 0~9
            code_list.append(str(i))
    if mode >= 2 or 0:
        for i in range(97, 123):  # a-z
            code_list.append(chr(i))
    if mode >= 3 or 0:
        for i in range(65, 91):  # A-Z
            code_list.append(chr(i))
    code = sample(code_list, lenguth)  # 随机取指定位数
    code_num = "".join(code)
    return code_num


def gen_md5_password(password: str, salt: str = None):
    """
    MD5生成（支持加盐）
    """
    salted_passowrd = f"{password}{salt}"
    return md5(salted_passowrd.encode("utf-8")).hexdigest()
    
def gen_gravatar_url(email: str):
    return "https://cn.gravatar.com/avatar/{}".format(
            md5(email.encode("utf-8")).hexdigest())