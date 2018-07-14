# virtual judge 爬虫

目前支持OJ：

- [hdu](http://acm.hdu.edu.cn/)
- [poj](http://poj.org/)
- [codeforces](http://codeforces.com/)

使用方式：

有三个环境变量可以配置，配置方式如下：
```python
import os
# 超时秒数
HTTP_METHOD_TIMEOUT = os.getenv('HTTP_METHOD_TIMEOUT', 10)

# 获取结果次数
RESULT_COUNT = os.getenv('RESULT_COUNT', 20)

# 每两次获取结果之间间隔 / s
RESULT_INTERVAL = os.getenv('RESULT_INTERVAL', 1)
```

考虑开发成pip包的形式, 所以如下方式引入：

`from OJcrawler.control import Controller`



爬取HDU的1033号题目的题面信息：
```
>>> from control import Controller
>>> hdu = Controller('hdu', 'handle', 'password')
>>> hdu.get_problem(1033)
(True, 
    {'title': 'Edge', 
    'judge_os': 'Windows', 
    'time_limit': {'default': 1000, 
                   'java': 2000}, 
    'memory_limit': {'default': 32768, 
                     'java': 65536}, 
    'problem_type': 'regular',
    'description': {string of html}
    'input_description': {string of html}
    'output_description': {string of html}
    'input_sample': {string list}
    'output_sample': {string list}, length equal to input_sample
    'source': {string of html}
    ...
)
```