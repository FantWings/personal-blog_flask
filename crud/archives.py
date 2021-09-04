from sql import session as sql
from sql.t_archive import t_archive

from utils.covert import toTimeStamp
from utils.log import log
from .auth import loginRequired
from .tag import mapTags, getTagsList, unmapTags


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
            "tags": getTagsList(archive.id),
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
    archive = sql.query(t_archive).filter_by(id=archId).one_or_none()
    if int(uid) is not archive.author_id:
        return {"status": 1, "msg": "你不能删除不属于你的文章"}
    # 解除和文章相关的外键
    unmapTags(archId)
    # 删除目标文章
    sql.delete(archive)
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
