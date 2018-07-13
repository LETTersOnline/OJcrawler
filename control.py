# -*- coding: utf-8 -*-
# Created by crazyX on 2018/7/12
from crawlers import supports
from crawlers.include.utils import RESULT_COUNT, RESULT_INTERVAL
from crawlers.include.sync import sync_status

from time import sleep


class Controller(object):
    # 一次性根据配置的账号数量，初始化对应oj对应数量的Controller
    # 在外部做负载均衡
    def __init__(self, oj_name: str, handle: str, password: str):
        if oj_name.lower() not in supports.keys():
            raise NotImplementedError
        self.oj = supports[oj_name.lower()](handle, password)

    def get_problem(self, pid):
        return self.oj.get_problem(pid)

    def submit_code(self, pid, source, lang):
        return self.oj.submit_code(pid, source, lang)

    def get_result(self):
        return self.oj.get_result()

    def get_result_by_rid(self, rid):
        return self.oj.get_result_by_rid(rid)

    @property
    def uncertain_result_status(self):
        return self.oj.uncertain_result_status

    def run(self, pid, source, lang, url=None, token=None, sid='sid'):
        # 一般来说只需要调用这个函数去提交代码以及获得结果
        # 固定次数和间隔轮询
        # url,token,sid都是用来同步结果
        success, dat = self.submit_code(pid, source, lang)
        if not success:
            return False, dat
        sync_status(url, token, sid, 'submitted')
        cnt = 0
        while cnt < RESULT_COUNT:
            sleep(RESULT_INTERVAL)
            success, info = self.get_result_by_rid(dat)
            if success:
                sync_status(url, token, sid, info)
            if str(info).lower() not in self.uncertain_result_status:
                return True, info
            cnt = cnt + 1

        sync_status(url, token, sid, 'fetch failed')
        return False, '获取运行结果失败'
