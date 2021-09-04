from sql import session as sql
from sql.t_tag import t_tag
from sql.t_archive_tag_map import t_archive_tag_map


def mapTags(tagList, archId):
    """关联标签"""
    for tag in tagList:
        sql.add(
            t_archive_tag_map(
                tag_id=sql.query(t_tag).filter_by(name=tag).one_or_none()
                or addNewTag(tag),
                arch_id=archId,
            )
        )
    sql.commit()


def addNewTag(tag):
    """添加标签"""
    newTags = t_tag(name=tag)
    sql.add(newTags)
    sql.commit()
    return newTags.id


def getTagsList(archId):
    """查询标签"""
    mapObj = sql.query(t_archive_tag_map).filter_by(arch_id=archId).all()
    tagList = []
    for map in mapObj:
        tagList.append(map.tag.name)
    return tagList
