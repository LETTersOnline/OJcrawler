# -*- coding: utf-8 -*-
# Created by crazyX on 2018/7/14

from crawlers.base import OJ
from crawlers.include.utils import logger, save_static_file
from crawlers.include.utils import HTTP_METHOD_TIMEOUT


class Codeforces(OJ):
    # cf和poj或者hdu有所不同，不同题目可能有限制提交的语言

    def __init__(self, handle, password):
        super().__init__(handle, password)

    @property
    def browser(self):
        pass

    @property
    def url_home(self):
        pass

    def url_problem(self, pid):
        pass

    @property
    def url_login(self):
        pass

    @property
    def url_submit(self):
        pass

    @property
    def url_status(self):
        pass

    @property
    def http_headers(self):
        pass

    @property
    def problem_fields(self):
        pass

    @property
    def uncertain_result_status(self):
        pass

    @property
    def problem_sample_fields(self):
        pass

    def post(self, url, data):
        pass

    @property
    def get_languages(self):
        pass

    def login(self):
        pass

    def is_login(self):
        pass

    def replace_image(self, html):
        pass

    def get_problem(self, pid):
        pass

    def submit_code(self, pid, source, lang):
        pass

    def get_result(self):
        pass