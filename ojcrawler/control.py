# -*- coding: utf-8 -*-
# Created by crazyX on 2018/7/12
# noinspection PyUnresolvedReferences
from __future__ import *

from ojcrawler.crawlers import supports
import inspect
from ojcrawler.utils import sample_save_image, sample_sync_func, submit_code


class Controller(object):

    # 😝不同OJ爬虫的同步状态函数和替换图片url函数已经被抽象为统一的函数
    def __init__(self, sync_func=sample_sync_func, image_func=sample_save_image):
        # 这个函数用来同步状态，必须为sync_func(status, *args, **kwargs) 形式xw
        args = inspect.getargspec(sync_func)[0]
        if len(args) < 1 or args[0] != 'data':
            raise ValueError('sync_func的第一个参数必须为data而不是{}, '
                             'sample: sync_func(data, *args, **kwargs)'.format(args[0]))

        args = inspect.getargspec(image_func)[0]
        if len(args) != 2:
            raise ValueError('image_func必须为两个参数')
        if args[0] != 'image_url' or args[1] != 'oj_name':
            raise ValueError('image_func的两个参数必须为image_url({})和oj_name({}), '
                             'sample: sample_save_image(image_url, oj_name)'.format(args[0], args[1]))

        self.sync_func = sync_func
        self.image_func = image_func

        self.static_supports = {}
        self.accounts = {}

        for key in supports.keys():
            self.static_supports[key] = supports[key]('static', 'static', image_func)

    @staticmethod
    def supports():
        return supports.keys()

    def update_account(self, oj_name, handle, password):
        if oj_name not in supports.keys():
            raise NotImplementedError('oj_name only supports: {}'.format(str(supports.keys())))
        self.accounts[oj_name] = (handle, password)

    def get_languages(self, oj_name):
        if oj_name not in supports.keys():
            raise NotImplementedError('oj_name only supports: {}'.format(str(supports.keys())))
        return self.static_supports[oj_name].get_languages()

    def get_problem(self, oj_name, pid):
        if oj_name not in supports.keys():
            raise NotImplementedError('oj_name only supports: {}'.format(str(supports.keys())))
        return self.static_supports[oj_name].get_problem(pid)

    def submit_code(self, oj_name, source, lang, pid, *args, **kwargs):
        if oj_name not in supports.keys():
            raise NotImplementedError('oj_name only supports: {}'.format(str(supports.keys())))
        if oj_name not in self.accounts:
            raise EnvironmentError('you should update account first')
        handle, password = self.accounts[oj_name]
        return submit_code(oj_name, handle, password, self.image_func, self.sync_func, source, lang, pid, *args, **kwargs)

    @staticmethod
    def get_basic_language(oj_name):
        if oj_name not in supports.keys():
            raise NotImplementedError('oj_name only supports: {}'.format(str(supports.keys())))
        # 只考虑三种最基础的语言，用来在比赛当中避免选手根据源语言判断OJ来源
        # c, c++, java
        if oj_name == 'poj':
            return {
                'c': 'GCC',
                'c++': 'G++',
                'c++11': None,
                'java': 'JAVA',
            }
        elif oj_name == 'hdu':
            return {
                'c': 'GCC',
                'c++': 'G++',
                'c++11': 'G++',
                'java': 'JAVA',
            }

        elif oj_name == 'codeforces':
            return {
                'c': 'GNU GCC C11 5.1.0',
                'c++': 'GNU G++11 5.1.0',
                'c++11': 'GNU G++11 5.1.0',
                'java': 'Java 1.8.0_162',
            }

