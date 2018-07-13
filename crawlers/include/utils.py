# -*- coding: utf-8 -*-
# Created by crazyX on 2018/7/7
from logging.handlers import RotatingFileHandler
import os
import urllib
import urllib.request
import pathlib
import logging

logFile = 'judge.log'
my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5 * 1024 * 1024,
                                 backupCount=2, encoding=None, delay=0)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d]'
                           ' [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='judge.log',
                    filemode='w',
                    )

logging.getLogger('').addHandler(my_handler)

logger = logging

DEBUG = True

# 超时秒数
HTTP_METHOD_TIMEOUT = 10

# 获取结果次数
RESULT_COUNT = 20

# 每两次获取结果之间间隔 / s
RESULT_INTERVAL = 3

STATIC_OJ_ROOT = os.path.join(pathlib.Path(__file__).parent.parent, 'statics')
STATIC_OJ_URL = 'localhost:8000/statics/'


def save_static_file(static_file_url, save_folder, file_name=None):
    # 保存静态文件，并返回新的url
    if not file_name:
        file_name = static_file_url.split('/')[-1]
    path = os.path.join(save_folder, file_name)
    req = urllib.request.Request(static_file_url)
    resp = urllib.request.urlopen(req)
    data = resp.read()
    with open(path, 'wb') as fp:
        fp.write(data)
    return STATIC_OJ_URL + file_name
