# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)

from ojcrawler.crawlers.config import *
from ojcrawler.crawlers import supports
from time import sleep
import json


def sample_sync_func(data, *args, **kwargs):
    # 多余的对应参数应该在add_task的时候按顺序传入
    # data = {
    #     'status': '各oj对应的状态字符串',
    #     'established': True,  # False, 表明是否是确定的状态，如果是，应该还有额外的信息
    #     'rid': trs[1].contents[0].text.strip(),
    #     'time': trs[1].contents[4].text.strip(),
    #     'memory': trs[1].contents[5].text.strip(),
    #     'ce_info': '',
    # }
    json_data = json.dumps(data)
    print(args, kwargs)
    logger.info("data: " + json_data)


def sample_save_image(image_url, oj_name):
    # 传入一个图片的地址，返回新的地址
    # oj_name 会传入oj自身的名字，方便用来分类
    # 1. 可以将图片保存到本地然后返回静态服务器的地址
    # 2. 可以上传到某图云然后返回图云的地址
    # 3. 也可以直接返回源oj的地址，这样如果不能访问外网就存在风险
    print(oj_name, image_url)
    return image_url


def submit_code(oj_name, handle, password, image_func, sync_func, source, lang, pid, *args, **kwargs):
    """
    提交代码核心函数
    :param oj_name:     OJ名，需要在support oj list中
    :param handle:      对应oj的用户名
    :param password:    对应oj的密码
    :param image_func:  图片保存函数，参考sample_save_image
    :param sync_func:   状态同步函数，参考sample_sync_func
    :param source:      源代码
    :param lang:        语言
    :param pid:         题目题号
    :param args:        传入状态同步函数的参数
    :param kwargs:      传入状态同步函数的参数
    :return:
    """
    oj =  supports[oj_name](handle, password, image_func)
    success, dat = oj.submit_code(source, lang, pid)

    def sync(data):
        return sync_func(data, *args, **kwargs)

    if not success:
        logger.warning('{} - {}'.format(oj.oj_name, dat))
        sync({'status': 'submit failed', 'established': True})
        return False, dat

    sync({'status': 'submitted', 'established': False})

    pre_status = 'submitted'
    cnt = 0
    fetch_success = False
    while cnt < RESULT_COUNT:
        sleep(RESULT_INTERVAL)
        success, info = oj.get_result_by_rid(dat)
        if success:
            status = info['status']
            if status != pre_status:
                # 注意codeforces
                established = True
                for uncertain_status in oj.uncertain_result_status:
                    if uncertain_status in str(status).lower():
                        established = False
                info['established'] = established
                sync(info)
                pre_status = status
                if established:
                    fetch_success = True
                    break
        cnt = cnt + 1

    if not fetch_success:
        sync({'status': 'fetch failed', 'established': False})
        return False, "获取运行结果失败"
    return True, ""
