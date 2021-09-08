from flask import request
from . import archiveAPI
from utils.log import log

from utils.response import json_res
from crud.archives import *
from crud.comment import *

log("Loaded ArchiveAPI [Ver 1.1]")


@archiveAPI.route("/getList", methods=["GET"])
def getArchivesList():
    """
    获取博客列表
    """
    limit = request.args.get("limit", 10)
    result = queryArchiveList(limit=int(limit))
    return json_res(**result)


@archiveAPI.route("/getTags", methods=["GET"])
def getArchivesTags():
    """
    获取标签列表
    """
    return json_res(data=["test", "test2"])


@archiveAPI.route("/getDetail/<archId>", methods=["GET"])
def getArchivesDetail(archId):
    """
    获取文章内容
    """
    if not archId:
        return json_res(msg="无效的文章ID", status=1)
    result = queryArchive(archId)
    return json_res(**result)


@archiveAPI.route("/add", methods=["POST"])
def apiAddArchive():
    """添加文章"""
    body = request.get_json()
    result = addArchive(**body)
    return json_res(**result)


@archiveAPI.route("/update", methods=["POST"])
def apiUpdateArchive():
    """修改文章"""
    archId = request.args.get("archId")
    body = request.get_json()
    result = updateArchive(archId, **body)
    return json_res(**result)


@archiveAPI.route("/delete", methods=["POST"])
def apiDeleteArchive():
    """删除文章"""
    archId = request.args.get("archId")
    result = deleteArchive(archId)
    return json_res(**result)


@archiveAPI.route("/comment", methods=["GET", "POST", "DELETE"])
def apiCommentArchive():
    """评论文章"""
    archId = request.args.get("archId")
    if request.method == "GET":
        result = queryComment(archId)

    if request.method == "POST":
        body = request.get_json()
        result = addComment(archId, **body)

    if request.method == "DELETE":
        comment_id = request.args.get("comment_id")
        result = deleteComment(comment_id=comment_id)

    return json_res(**result)
