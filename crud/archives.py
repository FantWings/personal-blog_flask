from sql import session as sql
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
    archive = sql.query(t_archive).filter_by(id=archId).one_or_none()

    try:
        archive.views = archive.views + 1
        sql.flush()
        data = {
            "title": archive.title,
            "author": archive.author.nickname,
            "author_uuid": archive.author.uuid,
            "content": archive.content,
            "coverImage": archive.cover_image,
            "createTime": toTimeStamp(archive.create_time),
            "updateTime": toTimeStamp(archive.update_time),
            "views": archive.views,
        }
        sql.commit()
        log("Opened Archive: 《{}》, visited: {}".format(archive.title, archive.views))
    except AttributeError:
        log("Client requested unexist archive, ID={}".format(archId), "warn")
        return {"status": 2, "msg": "请求的文章不存在或被删除"}
    except Exception as e:
        return {"status": 5, "msg": e}

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
    sql.add(newArchive)
    sql.flush()
    mapTags(tags, newArchive.id)
    sql.commit()

    return {"status": 0}


@loginRequired
def deleteArchive(uid, archId):
    """删除一个文章"""
    query = t_archive.query.filter_by(id=archId).first()
    if int(uid) is not query.author_id:
        return {"status": 1, "msg": "你不能删除不属于你的文章"}
    sql.delete(query)
    sql.commit()

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

    sql.add(query)
    sql.commit()

    return {"status": 0}


@loginRequired
def addComment(uid, archId, comment):
    """添加评论"""
    if len(comment) <= 0:
        return {"status": 2, "msg": "评论内容不可为空"}
    addComment = t_comment(arch_id=archId, user_id=uid, comment=comment)
    sql.add(addComment)
    sql.commit()
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
