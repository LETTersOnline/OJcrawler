# -*- coding: utf-8 -*-
# Created by crazyX on 2018/7/7
from crawlers.include.utils import DEBUG
import requests


def sync_status(url, token, sid, status):
    # print address, sid, status
    headers = {"Content-Type": "application/json"}
    data = {
        'token': token,
        'result': status,
        'submission_id': sid,
    }
    try:
        if not DEBUG and url:
            info = requests.post(url, headers=headers, json=data, timeout=2).json()
            print(info)
        else:
            print(url, token, sid, status)
        # logger.info(str(info))
    except Exception as e:
        print(e)
        # logger.exception(e)
