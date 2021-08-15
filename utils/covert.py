# 时间戳转换函数
def toTimeStamp(format_time):
    import time
    # print(format_time)
    # # timeArry = time.strptime(format_time, "%Y-%m-%d %H:%M:%S")
    # print("{}=>{}".format(time, timeArry))
    timeStamp = int(time.mktime(format_time.timetuple())) * 1000
    return timeStamp


# 查询结果转换函数
def sqlToJson(result):
    dict = result.__dict__
    if "_sa_instance_state" in dict:
        del dict["_sa_instance_state"]
    if "create_time" in dict:
        dict['create_time'] = toTimeStamp(dict['create_time'])
    if "update_time" in dict:
        dict['update_time'] = toTimeStamp(dict['update_time'])
    return dict
