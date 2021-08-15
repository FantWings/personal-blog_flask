from sql import db
from sql.t_archives import t_archives
from sql.t_tags import t_tags
from sql.t_tags_archives import t_tags_archives
from utils.covert import toTimeStamp
from utils.log import log
from utils.covert import sqlToJson


def queryArchiveList():
    archives = t_archives.query.with_entities(
        t_archives.id,
        t_archives.preview,
        t_archives.cover_image,
        t_archives.time_for_read,
        t_archives.title,
        t_archives.update_time,
        t_archives.views,
    ).all()
    tags = t_tags.query.with_entities(t_tags.name).all()
    # ref = t_tags_archives.query.all()
    # print(ref)
    data = []
    for result in archives:
        data.append(
            {
                "cover_image": result.cover_image,
                "id": result.id,
                "preview": result.preview,
                "time_for_read": result.time_for_read,
                "title": result.title,
                "update_time": toTimeStamp(result.update_time),
                "views": result.views,
                # "tags": tags
            }
        )
    return {"data": data}


def queryArchive(archId):
    query = t_archives.query.filter_by(id=archId).first()
    data = sqlToJson(query)
    log("Opened Archive: 《{}》".format(data.get("title", "undefined")))
    return {"data": data}
