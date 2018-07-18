# -*- coding: utf-8 -*-
# Created by crazyX on 2018/7/7
from crawlers.poj import POJ
from crawlers.hdu import HDU
from crawlers.codeforces import Codeforces

supports = {
    'poj': POJ,
    'hdu': HDU,
    'codeforces': Codeforces,
}

static_supports = {
    'poj': POJ('static', 'static'),
    'hdu': HDU('static', 'static'),
    'codeforces': Codeforces('static', 'static'),
}
