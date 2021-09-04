from sql import db
from sql.t_archive import t_archive
from sql.t_comment import t_comment

# from sql.t_user import t_user

from utils.covert import toTimeStamp
from utils.log import log
from .auth import loginRequired
from .tag import mapTags, getTagsList


def queryArchiveList():
    """查询博客列表"""
    archives = t_archive.query.all()
    data = []
    for result in archives:
        data.append(
            {
                "cover_image": result.cover_image,
                "id": result.id,
                "preview": result.content[:300].split("\n\n"),
                "time_for_read": result.time_for_read,
                "title": result.title,
                "update_time": toTimeStamp(result.update_time),
                "views": result.views,
                "content": result.content,
                "author": {
                    "username": result.author.nickname,
                    "avatar": result.author.avatar,
                },
                "tags": getTagsList(result.id),
            }
        )
    return {"data": data}


def queryArchive(archId):
    """查询博客详细内容"""
    query = t_archive.query.filter_by(id=archId).first()
    if query is None:
        log("Client requested unexist archive, ID={}".format(archId), "warn")
        return {"status": 1, "msg": "请求的文章不存在或被删除"}
    data = {
        "title": query.title,
        "author": query.author.nickname,
        "author_uuid": query.author.uuid,
        "content": query.content,
        "coverImage": query.cover_image,
        "createTime": toTimeStamp(query.create_time),
        "updateTime": toTimeStamp(query.update_time),
        "views": query.views,
    }
    log("Opened Archive: 《{}》".format(data.get("title", "undefined")))
    return {"data": data}


@loginRequired
def addArchive(uid, title, content, cover_image, tags, time_for_read=5):
    """添加一个新文章"""
    newArchive = t_archive(
        title=title,
        content=content,
        cover_image=cover_image,
        time_for_read=time_for_read,
        author_id=uid,
    )
    db.session.add(newArchive)
    db.session.flush()
    mapTags(tags, newArchive.id)
    db.session.commit()

    return {"status": 0}


@loginRequired
def deleteArchive(uid, archId):
    """删除一个文章"""
    query = t_archive.query.filter_by(id=archId).first()
    if int(uid) is not query.author_id:
        return {"status": 1, "msg": "你不能删除不属于你的文章"}
    db.session.delete(query)
    db.session.commit()

    return {"status": 0}


@loginRequired
def updateArchive(uid, archId, title, content, cover_image, tags, time_for_read=5):
    """更新一个文章"""
    query = t_archive.query.filter_by(id=archId).first()
    if uid is not query.author_id:
        return {"status": 1, "msg": "你不能修改不属于你的文章"}
    query.title = title
    query.content = content
    query.cover_image = cover_image
    query.time_for_read = time_for_read

    db.session.add(query)
    db.session.commit()

    return {"status": 0}


@loginRequired
def addComment(uid, archId, comment):
    """添加评论"""
    if len(comment) <= 0:
        return {"status": 2, "msg": "评论内容不可为空"}
    addComment = t_comment(arch_id=archId, user_id=uid, comment=comment)
    db.session.add(addComment)
    db.session.commit()
    return {"status": 0}


def queryComment(archId):
    """查询评论"""
    comments = (
        t_comment.query.filter_by(arch_id=archId)
        .order_by(t_comment.create_time.desc())
        .all()
    )
    data = []
    for result in comments:
        data.append(
            {
                "id": result.id,
                "nickname": result.user.nickname,
                "avatar": result.user.avatar,
                "comment": result.comment,
                "time": toTimeStamp(result.create_time),
            }
        )
    return {"data": data}
