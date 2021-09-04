from sql import session as sql
from sql.t_comment import t_comment
from .auth import loginRequired
from utils.covert import toTimeStamp


def queryComment(archId):
    """查询评论"""
    comments = (
        t_comment.query.filter_by(arch_id=archId)
        .order_by(t_comment.create_time.desc())
        .all()
    )
    data = []
    for comment in comments:
        data.append(
            {
                "id": comment.id,
                "owner": comment.user.uuid,
                "nickname": comment.user.nickname,
                "avatar": comment.user.avatar,
                "comment": comment.comment,
                "time": toTimeStamp(comment.create_time),
            }
        )
    return {"data": data}


@loginRequired
def addComment(uid, archId, comment):
    """添加评论"""
    if len(comment) <= 0:
        return {"status": 2, "msg": "评论内容不可为空"}
    newComment = t_comment(arch_id=archId, user_id=uid, comment=comment)
    sql.add(newComment)
    sql.commit()
    return {"status": 0}


@loginRequired
def deleteComment(uid, comment_id):
    """删除评论"""
    target = sql.query(t_comment).filter_by(id=comment_id, user_id=uid).one_or_none()
    sql.delete(target)
    sql.commit()
    return {"status": 0}
