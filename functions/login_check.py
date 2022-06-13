from flask import request
from functools import wraps
from utils.redis import Redis

def login_required(func):
    """
    装饰器函数，用来验证用户登录态
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 从HEADER取得TOKEN，验证token是否为空
        try: 
            token = request.headers["token"]
        except Exception:
            return {"status":1, "msg": "请求参数有误"}
        
        # 使用token从redis中读取用户ID
        uid = Redis.read(f"{token}/uid")
        if uid is None:
            return {"status": 10, "msg": "该请求需要登录"}

        # 刷新Token有效期
        Redis.expire(f"{token}/uid")
        return func(uid, *args, **kwargs)
    return wrapper