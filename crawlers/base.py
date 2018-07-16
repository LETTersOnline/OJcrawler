# -*- coding: utf-8 -*-
# Created by crazyX on 2018/7/8
from socket import timeout
from urllib.error import URLError, HTTPError
from crawlers.config import logger, save_image
from crawlers.config import HTTP_METHOD_TIMEOUT


class OJ(object):
    # 每一个账号同一时间只考虑交一道题目，这样可以有效避免查封，且方便处理
    # image_func 用来做网页中图片的url替换
    def __init__(self, handle, password, image_func):
        self.handle = handle
        self.password = password
        self.image_func = image_func

    def __str__(self):
        return "{}({})".format(self.oj_name, self.handle)

    @property
    def oj_name(self):
        return self.__class__.__name__

    # 以下为基础属性
    @property
    def browser(self):
        raise NotImplementedError

    @property
    def url_home(self):
        raise NotImplementedError

    def url_problem(self, pid):
        raise NotImplementedError

    @property
    def url_login(self):
        raise NotImplementedError

    @property
    def url_submit(self):
        raise NotImplementedError

    @property
    def url_status(self):
        raise NotImplementedError

    @property
    def http_headers(self):
        raise NotImplementedError

    @property
    def problem_fields(self):
        raise NotImplementedError

    @property
    def uncertain_result_status(self):
        raise NotImplementedError

    @property
    def compatible_problem_fields(self):
        # time limit 数字，单位为 ms
        # memory limit 数字，单位为 kb
        # origin 为题目链接字符串
        # input/output sample 为有序列表，长度相同
        # 三个description和hint，source为html源码，并替换了其中的image路径为本地路径
        # 其余为字符串

        # 需要额外考虑一下针对不同语言的不同的time limit和memory limit
        # time_limit = {
        #   'default': 1000,
        #   'java': 3000,
        # }
        # memory_limit = {
        #   'default': 65536,
        # }

        # problem_type为字符串，表示题目类型，默认为'regular', 可选为'special judge'等

        return ['title', 'judge_os', 'time_limit', 'memory_limit', 'problem_type', 'origin',
                'description', 'input_description', 'output_description', 'hint', 'source',
                'input_sample', 'output_sample',
                ]

    @property
    def problem_sample_fields(self):
        # 只需要text内容，并转为list存储
        raise NotImplementedError

    # 以下为基础函数
    def get(self, url):
        try:
            return self.browser.open(url, timeout=HTTP_METHOD_TIMEOUT)
        except (HTTPError, URLError) as error:
            logger.error('Data not retrieved because %s\nURL: %s', error, url)
            return None
        except timeout:
            logger.error('socket timed out\nURL: %s', url)
            return None

    def post(self, url, data):
        raise NotImplementedError

    @staticmethod
    def http_status_code(response):
        return response.status if response else None

    def ping(self):
        # 5s是否能访问主页
        response = self.get(self.url_home)
        return self.http_status_code(response) == 200

    # 以下为OJ行为函数
    @staticmethod
    def batch_register(self):
        pass

    @property
    def get_languages(self):
        # 获取语言列表
        # example:
        # LANGUAGE = {
        #     'G++': '1',
        #     'G++11': '42',
        #     'G++14': '50',
        #     'GCC': '10',
        #     'JAVA': '36',
        #     'PYTHON2': '7',
        #     'PYTHON3': '31',
        # }
        raise NotImplementedError

    def login(self):
        raise NotImplementedError

    def is_login(self):
        raise NotImplementedError

    def replace_image(self, html):
        raise NotImplementedError

    def get_problem(self, pid):
        raise NotImplementedError

    def submit_code(self, pid, source, lang):
        # 返回 run id
        raise NotImplementedError

    def get_result(self):
        # 只需要获取最近一次提交的结果
        # 如果遇到了什么异常，考虑直接重新提交
        raise NotImplementedError

    def get_result_by_rid(self, rid):
        # 这个不一定每个系统都能实现
        pass

    def get_compile_error_info(self, rid):
        # 这个不一定每个系统都能实现
        pass
