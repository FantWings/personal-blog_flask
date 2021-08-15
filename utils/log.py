import time
from os import getenv


def log(content, level='info'):
    # methods = {
    #     "defualt": 0,
    #     "high_light": 1,
    #     "under_line": 4,
    #     "flashing": 5,
    #     "invert": 7,
    #     "invistable": 8
    # }
    # colors = {
    #     "black": 0,
    #     "red": 1,
    #     "green": 2,
    #     "yellow": 3,
    #     "blue": 4,
    #     "purple": 5,
    #     "cyan": 6,
    #     "white": 7
    # }

    logLevels = {
        "debug": 0,
        "info": 1,
        "warn": 2,
        "error": 3,
        "nolog": 4,
    }

    if logLevels[getenv('LOG_LEVEL', default='error')] > logLevels[level]:
        return None

    fontColor = {"info": 2, "warn": 3, "error": 1, 'debug': 5}
    template = {
        "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "loglevel": level.upper(),
        "content": content,
        "printMethod": 0,
        "fontColor": fontColor.get(level),
    }

    print(
        "\033[{printMethod};3{fontColor}m[{time}][{loglevel}] {content}\033[0m"
        .format(**template))
