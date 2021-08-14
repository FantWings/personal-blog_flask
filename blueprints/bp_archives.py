from flask import Blueprint, request, make_response
from . import archiveAPI

from utils.response import json_res
from crud.archives import queryArchiveList, queryArchive

print('[INFO] Blueprint - archiveAPI Loaded.')


@archiveAPI.route('/getArchivesList', methods=["GET"])
def getArchivesList():
    """
    获取博客列表
    """
    result = queryArchiveList()
    return json_res(**result)


@archiveAPI.route('/getArchivesTags', methods=["GET"])
def getArchivesTags():
    """
    获取标签列表
    """
    return json_res(data=['test', 'test2'])


@archiveAPI.route('/getArchivesDetail/<id>', methods=['GET'])
def getArchivesDetail(id):
    """
    获取文章内容
    """
    archId = request.args.get('id')
    if not archId:
        return json_res(msg="无效的文章ID", status=1)
    result = queryArchive(archId)
    return json_res(**result)