from sql import db
from sql.t_archives import t_archives

# from sql.t_tags import t_tags
# from sql.t_tags_archives import t_tags_archives
# from sql.t_user import t_user
from utils.covert import toTimeStamp
from utils.log import log
from utils.covert import toTimeStamp
from .auth import loginRequired


def queryArchiveList():
    archives = t_archives.query.all()
    # tags = t_tags.query.with_entities(t_tags.name).all()
    # ref = t_tags_archives.query.all()
    # print(ref)
    data = []
    for result in archives:
        # print(result.content.split('\n\n'))
        data.append(
            {
                "cover_image": result.cover_image,
                "id": result.id,
                "preview": result.content[:30].split('\n\n')[1],
                "time_for_read": result.time_for_read,
                "title": result.title,
                "update_time": toTimeStamp(result.update_time),
                "views": result.views,
                "content": result.content,
                "author": {
                    "username": result.author.username,
                    "avatar": result.author.avatar,
                },
            }
        )
    return {"data": data}


def queryArchive(archId):
    query = t_archives.query.filter_by(id=archId).first()
    if query is None:
        log("Client requested unexist archive, ID={}".format(archId), "warn")
        return {"status": 1, "msg": "请求的文章不存在或被删除"}
    data = {
        "title": query.title,
        "author": query.author.username,
        "content": query.content,
        "coverImage": query.cover_image,
        "createTime": toTimeStamp(query.create_time),
        "updateTime": toTimeStamp(query.update_time),
        "views": query.views,
    }
    log("Opened Archive: 《{}》".format(data.get("title", "undefined")))
    return {"data": data}


@loginRequired
def addArchive(uid, title, content, cover_image="", time_for_read=5):
    newArchive = t_archives(
        title=title,
        content=content,
        cover_image=cover_image,
        time_for_read=time_for_read,
        author_id=uid,
    )
    db.session.add(newArchive)
    db.session.commit()

    return {"status": 0}


@loginRequired
def deleteArchive(uid, archId):
    query = t_archives.query.filter_by(id=archId).first()
    if int(uid) is not query.author_id:
        return {"status": 1, "msg": "你不能删除不属于你的文章"}
    db.session.delete(query)
    db.session.commit()

    return {"status": 0}


@loginRequired
def updateArchive(uid, archId, title, content, cover_image="", time_for_read=5):
    query = t_archives.query.filter_by(id=archId).first()
    if int(uid) is not query.author_id:
        return {"status": 1, "msg": "你不能修改不属于你的文章"}
    query.title = title
    query.content = content
    query.cover_image = cover_image
    query.time_for_read = time_for_read

    db.session.add(query)
    db.session.commit()

    return {"status": 0}
