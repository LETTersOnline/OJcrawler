# -*- coding: utf-8 -*-
# Created by crazyX on 2018/7/8
from crawlers.older.hdu import HDU, hdu_submit
from crawlers.older.poj import POJ, poj_submit
# 調用格式：
# xxx_submit(problem_id, language_name, src_code, url, token, sid)
# url, token, sid 用来向web server实时更新判题状态

crawlers = {
    'hdu': hdu_submit,
    'poj': poj_submit,
}

lang_choices = {
    'hdu': HDU.LANGUAGE.keys(),
    'poj': POJ.LANGUAGE.keys(),
}