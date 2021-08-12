import time


# 时间戳转换函数
def toTimeStamp(format_time):
    # print(format_time)
    # # timeArry = time.strptime(format_time, "%Y-%m-%d %H:%M:%S")
    # print("{}=>{}".format(time, timeArry))
    timeStamp = int(time.mktime(format_time.timetuple())) * 1000
    return timeStamp