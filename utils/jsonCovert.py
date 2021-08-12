from .timeCovert import toTimeStamp


def sqlToJson(result):
    dict = result.__dict__
    if "_sa_instance_state" in dict:
        del dict["_sa_instance_state"]
    if "create_time" in dict:
        dict['create_time'] = toTimeStamp(dict['create_time'])
    if "update_time" in dict:
        dict['update_time'] = toTimeStamp(dict['update_time'])
    return dict