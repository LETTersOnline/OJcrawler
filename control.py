# -*- coding: utf-8 -*-
# Created by crazyX on 2018/7/12
from crawlers import supports
from crawlers.include.utils import RESULT_COUNT, RESULT_INTERVAL, logger
import inspect
from time import sleep


def sample_sync_func(status, *args, **kwargs):
    logger.info("status: " + status)


def sample_save_image(image_url, oj_name):
    # 传入一个图片的地址，返回新的地址
    # oj_name 会传入oj自身的名字，方便用来分类
    # 1. 可以将图片保存到本地然后返回静态服务器的地址
    # 2. 可以上传到某图云然后返回图云的地址
    # 3. 也可以直接返回源oj的地址，这样如果不能访问外网就存在风险
    return image_url


class Controller(object):
    # 一次性根据配置的账号数量，初始化对应oj对应数量的Controller
    # 在外部做负载均衡

    def __init__(self, oj_name: str, handle: str, password: str,
                 sync_func=sample_sync_func,
                 image_func=sample_save_image):
        if oj_name.lower() not in supports.keys():
            raise NotImplementedError
        # 这个函数用来同步状态，必须为sync_func(status, *args, **kwargs) 形式
        args = inspect.getfullargspec(sync_func)[0]
        if len(args) < 1 or args[0] != 'status':
            raise ValueError('sync_func的第一个参数必须为status而不是{}, '
                             'sample: sync_func(status, *args, **kwargs)'.format(args[0]))

        args = inspect.getfullargspec(image_func)[0]
        if len(args) != 2:
            raise ValueError('image_func必须为两个参数')
        if args[0] != 'image_url' or args[1] != 'oj_name':
            raise ValueError('image_func的两个参数必须为image_url({})和oj_name({}), '
                             'sample: sample_save_image(image_url, oj_name)'.format(args[0], args[1]))

        self.sync_func = sync_func
        self.oj = supports[oj_name.lower()](handle, password)

    def get_problem(self, pid):
        return self.oj.get_problem(pid)

    def submit_code(self, pid, source, lang):
        return self.oj.submit_code(pid, source, lang)

    def get_result(self):
        return self.oj.get_result()

    def get_result_by_rid(self, rid):
        return self.oj.get_result_by_rid(rid)

    def get_compile_error_info(self, rid):
        return self.oj.get_compile_error_info(rid)

    @property
    def uncertain_result_status(self):
        return self.oj.uncertain_result_status

    @property
    def get_languages(self):
        return self.oj.get_languages

    def run(self, pid, source, lang, *args, **kwargs):
        # 一般来说只需要调用这个函数去提交代码以及获得结果
        # 固定次数和间隔轮询
        # args和kwargs都是用来给sync函数同步状态使用
        success, dat = self.submit_code(pid, source, lang)
        if not success:
            return False, dat
        self.sync_func('submitted', *args, **kwargs)
        cnt = 0
        while cnt < RESULT_COUNT:
            sleep(RESULT_INTERVAL)
            success, info = self.get_result_by_rid(dat)
            if success:
                status = info['status']
                self.sync_func(status, *args, **kwargs)
                if str(status).lower() not in self.uncertain_result_status:
                    return True, info
            cnt = cnt + 1

        self.sync_func('fetch failed', *args, **kwargs)
        return False, '获取运行结果失败'
