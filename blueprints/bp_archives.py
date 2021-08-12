from flask import Blueprint, request, make_response
from . import archiveAPI

from utils.response import json_res
from crud.archives import queryArchiveList

print('[INFO] Blueprint - archiveAPI Loaded.')


@archiveAPI.route('/getArchivesList', methods=["GET"])
def getArchivesList():
    """
    获取博客列表
    """
    # archId = request.args.get('id')
    # if not archId:
    #     return make_response(json_res(msg="无效的文章ID", status=1))
    results = queryArchiveList()
    return make_response(json_res(data=results))


@archiveAPI.route('/getArchivesTags', methods=["GET"])
def getArchivesTags():
    """
    获取标签列表
    """
    return make_response(json_res(data=['test', 'test2']))


@archiveAPI.route('/getArchivesDetail/<id>', methods=['GET'])
def getArchivesDetail(id):
    """
    获取文章内容
    """
    state = '占位'
    return make_response(json_res(data=state))