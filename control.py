# -*- coding: utf-8 -*-
# Created by crazyX on 2018/7/12
from crawlers import supports, static_supports
import inspect
from queue import Queue
from utils import sample_save_image, sample_sync_func, Worker


class Controller(object):

    # 😝不同OJ爬虫的同步状态函数和替换图片url函数已经被抽象为统一的函数
    def __init__(self, sync_func=sample_sync_func, image_func=sample_save_image):
        # 这个函数用来同步状态，必须为sync_func(status, *args, **kwargs) 形式
        args = inspect.getfullargspec(sync_func)[0]
        if len(args) < 1 or args[0] != 'data':
            raise ValueError('sync_func的第一个参数必须为data而不是{}, '
                             'sample: sync_func(data, *args, **kwargs)'.format(args[0]))

        args = inspect.getfullargspec(image_func)[0]
        if len(args) != 2:
            raise ValueError('image_func必须为两个参数')
        if args[0] != 'image_url' or args[1] != 'oj_name':
            raise ValueError('image_func的两个参数必须为image_url({})和oj_name({}), '
                             'sample: sample_save_image(image_url, oj_name)'.format(args[0], args[1]))

        self.sync_func = sync_func
        self.image_func = image_func

        self.queues = {}
        # 一个oj可能对应多个worker，{'poj': [instance1, instance2], 'hdu': [instance1]}
        self.workers = {}

        for key in supports.keys():
            self.queues[key] = Queue()
            self.workers[key] = []

    def __del__(self):
        self.stop()

    def _add_account(self, oj_name, handle, password):
        # 同一个oj重复handle只会采用第一个的配置
        worker = Worker(oj_name, handle, password, self.queues[oj_name], self.image_func, self.sync_func)
        # 可能是已经存在的实例
        if worker not in self.workers[oj_name]:
            self.workers[oj_name].append(worker)

    def init_accounts(self, accounts):
        # 初始化account信息，注意不能用重复的信息初始化
        # 注意会清空之前的账号信息
        for oj_name, handle, password in accounts:
            if oj_name not in supports.keys():
                raise NotImplementedError('oj_name only supports: {}'.format(str(supports.keys())))

        # 先停止所有的worker
        self.stop()
        # 创建对应的队列集和工作者集
        for key in supports.keys():
            self.queues[key] = Queue()
            self.workers[key] = []
        for oj_name, handle, password in accounts:
            self._add_account(oj_name, handle, password)
        return True

    def add_task(self, oj_name, pid, source, lang, *args):
        if oj_name not in supports.keys():
            raise NotImplementedError('oj_name only supports: {}'.format(str(supports.keys())))
        self.queues[oj_name].put((pid, source, lang, *args))

    def start(self):
        if not self.workers:
            raise RuntimeError('you should init accounts first.')
        for key in self.workers:
            for worker in self.workers[key]:
                worker.setDaemon(True)
                worker.start()

    def pause(self):
        for key in self.workers:
            for worker in self.workers[key]:
                worker.pause()

    def stop(self):

        for key in self.workers:
            for worker in self.workers[key]:
                assert type(worker) == Worker
                worker.stop()

        for key in self.queues.keys():
            cnt = len(self.workers[key])
            for i in range(cnt):
                self.queues[key].put(None)

        for key in self.workers:
            for worker in self.workers[key]:
                worker.join()

        # 清空worker和队列内存
        for queue in self.queues.values():
            with queue.mutex:
                queue.queue.clear()
            del queue
        for key in self.workers:
            for worker in self.workers[key]:
                del worker
        self.queues = {}
        self.workers = {}

    @staticmethod
    def get_languages(oj_name):
        if oj_name not in supports.keys():
            raise NotImplementedError('oj_name only supports: {}'.format(str(supports.keys())))
        return static_supports[oj_name].get_languages

    @staticmethod
    def get_problem(oj_name, pid):
        if oj_name not in supports.keys():
            raise NotImplementedError('oj_name only supports: {}'.format(str(supports.keys())))
        return static_supports[oj_name].get_problem(pid)
