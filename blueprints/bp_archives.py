from flask import request, Blueprint
from sqlalchemy import func
from Model import session as sql
from Model.t_archive import t_archive
from Model.t_comment import t_comment
from Model.t_tag import t_tag
from Model.t_archive_tag_map import t_archive_tag_map
from functions.login_check import login_required
from utils.response import json_response
from utils.covert import toTimeStamp

archiveAPI = Blueprint("archive", __name__, url_prefix="archive")

@archiveAPI.route("/getList", methods=["GET"])
def getArchivesList():
    """
    获取博客列表
    """
    limit = int(request.args.get("limit", 10))
    archives = (
    sql.query(t_archive)
    .order_by(t_archive.create_time.desc())
    .limit(limit)
    .all())
    
    data = []
    for result in archives:
        # 查询对应博文中的评论条目数
        query_comments_count = sql.query(func.count(t_comment.id)).filter_by(arch_id=result.id).scalar()
        data.append(
            {
                "id": result.id,
                "title": result.title,
                "create_time": toTimeStamp(result.create_time), 
                "update_time": toTimeStamp(result.update_time),
                "views": result.views,
                "comments": query_comments_count
            }
        )
    return json_response(data)


@archiveAPI.route("/getDetail/<archId>", methods=["GET"])
def getArchivesDetail(archId):
    """
    获取文章内容
    """
    if not archId:
        return json_response(msg="无效的文章ID", status=1)
    archive = sql.query(t_archive).filter_by(id=archId).one_or_none()

    def getTagsList(archId):
        """查询标签"""
        mapObj = sql.query(t_archive_tag_map).filter_by(arch_id=archId).all()
        tagList = []
        for map in mapObj:
            tagList.append(map.tag.name)
        return tagList

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
        
    except AttributeError:
        return json_response(status=2, msg="请求的文章不存在或被删除")
    except Exception as e:
        return json_response(status=5, msg=e)
    return json_response(data)


@archiveAPI.route("/add", methods=["POST"])
@login_required
def apiAddArchive(uid):
    """添加文章接口"""
    body = request.get_json()

    #添加新文章
    newArchive = t_archive(
        title=body["title"],
        content=body["content"],
        cover_image=body["cover_image"],
        time_for_read=body["time_for_read"],
        author_id=uid,
    )
    sql.add(newArchive)
    sql.flush()

    def addNewTag(tag):
        """添加标签"""
        newTags = t_tag(name=tag)
        sql.add(newTags)
        sql.commit()
        return newTags.id

    # 关联标签到文章上
    for tag in body["tags"]:
        target = t_archive_tag_map(
            tag_id= sql.query(t_tag).filter_by(name=tag).one_or_none() or addNewTag(tag),
            arch_id=newArchive.id,
        )
        sql.add(target)

    sql.commit()
    return json_response(status=0)



@archiveAPI.route("/update", methods=["POST"])
@login_required
def apiUpdateArchive(uid):
    """修改文章"""
    archId = request.args.get("archId")
    body = request.get_json()
    query = t_archive.query.filter_by(id=archId).first()
    if uid is not query.author_id:
        return json_response(status=1,msg="你不能修改不属于你的文章")

    try:
        query.title = body["title"]
        query.content = body["content"]
        query.cover_image = body["cover_image"]
        query.time_for_read = body["time_for_read"]
    except Exception:
        json_response(status=1,msg="请求参数有误")

    sql.add(query)
    sql.commit()
    return json_response(status=0)


@archiveAPI.route("/delete", methods=["POST"])
@login_required
def apiDeleteArchive(uid):
    """删除文章"""
    archId = request.args.get("archId")
    archive = sql.query(t_archive).filter_by(id=archId).one_or_none()
    if int(uid) is not archive.author_id:
        return {"status": 1, "msg": "你不能删除不属于你的文章"}
    # 解除和文章相关的外键
    tagMaps = sql.query(t_archive_tag_map).filter_by(arch_id=archId).all()
    for target in tagMaps:
        sql.delete(target)
    # 删除目标文章
    sql.delete(archive)
    sql.commit()
    return json_response(status=0)


@archiveAPI.route("/comment", methods=["GET"])
def apiCommentRead():
    """评论查询接口"""
    archId = request.args.get("archId")
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
    return json_response(data)



@archiveAPI.route("/comment", methods=["POST", "DELETE"])
@login_required
def apiCommentWrite(uid):
    """评论增删改接口"""
    if request.method == "POST":
        body = request.get_json()
        arch_id = request.args.get("archId")
        if body["comment"] is None:
            return json_response(status=2,msg="评论内容不可为空")
        newComment = t_comment(arch_id=arch_id, user_id=uid, comment=body["comment"])
        sql.add(newComment)

    if request.method == "DELETE":
        comment_id = request.args.get("comment_id")
        target = sql.query(t_comment).filter_by(id=comment_id, user_id=uid).one_or_none()
        sql.delete(target)

    sql.commit()
    return json_response(status=0)
    

