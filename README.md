# virtual judge 爬虫

目前支持OJ：

- [hdu](http://acm.hdu.edu.cn/)
- [poj](http://poj.org/)
- [codeforces](http://codeforces.com/)

## 架构
生产者消费者模型

对于每个账号，生成对应的`worker`，`Controller`和`worker`间通过每个oj对应的`queue`通信，`worker`从`queue`中按顺序获取`source, lang, pid, *args`参数，这些参数都由`Controller.add_task(oj_name, source, lang, pid, *args)`放入对应oj的队列当中

其中：
- oj_name: oj名称缩写，目前支持['hdu', 'poj', 'codeforces']
- source：源代码
- lang:  语言名称，可以通过`Controller.get_languages(oj_name).keys()`获取完整的可选列表, 或者`Controller.get_basic_language('oj_name')` 获取基础的几种语言的对应关系。
- pid: 题号，特别的，对于codeforces，题号应该是这样的形式：'112A'， '13a1'，以第一个非数字字符作为切分标准
- args：多余的args是用来配合同步状态的，参考同步状态部分。

## Controller(sync_func, image_func)
Controller实例化的时候可以额外传入两个函数，以下分别介绍。
### 同步状态(sync_func)
sample：
```python
import json
import logging as logger
def sample_sync_func(data, *args):
    # 多余的对应参数应该在add_task的时候按顺序传入
    # data = {
    #     'status': '各oj对应的状态字符串',
    #     'established': True,  # False, 表明是否是确定的状态，如果是，应该还有额外的信息
    #     'rid': 123124,
    #     'status': running,
    #     'time':           // 单位为ms
    #     'memory':         // 单位为kb
    # }
    json_data = json.dumps(data)
    logger.info("data: " + json_data)
```
多余的参数可以有提交的ID，web端的ip地址，认证token等等，按顺序传入后利用它们调用远端的接口更新对应提交的状态。

这些多余的参数应该按照同样的顺序在`add_task`的时候传入。

### 图片函数(image_func)

这个函数用来处理题面中含有的图片，对于远端oj上的图片，有不限于以下三种方式来处理：

- 直接使用源oj地址：优点是方便，缺点是图片显示受源oj网络状况限制
- 使用cdn服务缓存图片：优点是一般情况下比较稳定，但是在要求断外网（如比赛时）时比较僵硬
- 将图片下载到本地，利用本地静态服务器提供服务，可以满足一般需求，但是需要考虑缓存算法，什么时候更新，怎样更新本地文件是关键

sample：
```python
def sample_save_image(image_url, oj_name):
    return image_url
```
sample即第一种方式，这个函数会传入两个参数，一个是源oj的原始图片url，另外一个是oj名，可用于协助分类

## 使用方式

所有oj的提交、题面获取、结果获取等全部使用`Controller`来控制，`Controller`需要先用各个oj的账号信息初始化，对于每个oj的每个账号，会生成一个唯一的worker，注意，如果一个oj存在多个同名账号，以最先出现的为准。

调用`Controller.load_accounts_json(json_path)`将会从对应路径的json文件中读取账号信息，参考tests/accounts_sample.json的格式。


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

安装：切换到setup.py所在目录下：
```
python setup.py build
python setup.py install
```

考虑开发成pip包的形式, 所以如下方式引入：

`from ojcrawler.control import Controller`


一些操作示范：

```
>>> from control import Controller
>>> c = Controller()
>>> c.get_problem('hdu', '1033') # 获取hdu1033的题面信息
(True, 
    {
    'title': 'Edge', 
    'problem_type': 'regular', 
    'origin': 'http://acm.hdu.edu.cn/showproblem.php?pid=1033', 
    'time_limit': {'default': 1000, 'java': 2000}, 
    'memory_limit': {'default': 32768, 'java': 65536}, 
    'samples_input': ['V\nAVV'], 
    'samples_output': ['300 420 moveto\n310 420 lineto\n310 430 lineto\nstroke\nshowpage\n300 420 moveto\n310 420 lineto\n310 410 lineto\n320 410 lineto\n320 420 lineto\nstroke\nshowpage'], 
    'descriptions': [
        ('Problem Description', '<div class="panel_content">For products that are wrapped in small packings it is necessary that the sheet of paper containing the directions for use is folded until its size becomes small enough. We assume that a sheet of paper is rectangular and only folded along lines parallel to its initially shorter edge. The act of folding along such a line, however, can be performed in two directions: either the surface on the top of the sheet is brought together, or the surface on its bottom. In both cases the two parts of the rectangle that are separated by the folding line are laid together neatly and we ignore any differences in thickness of the resulting folded sheet. <br/>After several such folding steps have been performed we may unfold the sheet again and take a look at its longer edge holding the sheet so that it appears as a one-dimensional curve, actually a concatenation of line segments. If we move along this curve in a fixed direction we can classify every place where the sheet was folded as either type A meaning a clockwise turn or type V meaning a counter-clockwise turn. Given such a sequence of classifications, produce a drawing of the longer edge of the sheet assuming 90 degree turns at equidistant places.<br/></div>'), 
        ('Input', '<div class="panel_content">The input contains several test cases, each on a separate line. Each line contains a nonempty string of characters A and V describing the longer edge of the sheet. You may assume that the length of the string is less than 200. The input file terminates immediately after the last test case.<br/></div>'), 
        ('Output', '<div class="panel_content">For each test case generate a PostScript drawing of the edge with commands placed on separate lines. Start every drawing at the coordinates (300, 420) with the command "300 420 moveto". The first turn occurs at (310, 420) using the command "310 420 lineto". Continue with clockwise or counter-clockwise turns according to the input string, using a sequence of "x y lineto" commands with the appropriate coordinates. The turning points are separated at a distance of 10 units. Do not forget the end point of the edge and finish each test case by the commands stroke and showpage. <br/><br/>You may display such drawings with the gv PostScript interpreter, optionally after a conversion using the ps2ps utility.<br/><br/><center><img src="localhost:8000/statics/hdu/1033-1.gif" style="max-width:100%;"/></center><br/></div>'), 
        ('Recommend', '<div class="panel_content"></div>')
        ], 
    'category': '  University of Ulm Local Contest 2003  ', 
    'tags': [], 
    'append_html': ''
    }
)
>>> c.supports() # 查看当前支持的oj
dict_keys(['poj', 'hdu', 'codeforces'])
>>> c.get_languages('poj') # 查看poj所有支持的语言
{'G++': '0', 'GCC': '1', 'JAVA': '2', 'PASCAL': '3', 'C++': '4', 'C': '5', 'FORTRAN': '6'}
>>> c.get_basic_language('poj') # 查看基础的四种语言或配置在poj的中的映射
{'c': 'GCC', 'c++': 'G++', 'c++11': None, 'java': 'JAVA'}
```