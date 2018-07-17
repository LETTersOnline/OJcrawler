# -*- coding: utf-8 -*-
# Created by crazyX on 2018/7/14
from bs4 import BeautifulSoup
from robobrowser import RoboBrowser
from socket import timeout
from urllib.error import URLError, HTTPError
from crawlers.base import OJ
from crawlers.config import logger, save_image
from crawlers.config import HTTP_METHOD_TIMEOUT


class Codeforces(OJ):
    def __init__(self, handle, password, image_func=save_image):
        super().__init__(handle, password, image_func)

        self.rb = RoboBrowser(parser='html5lib')
        self.append_html = """
            <!-- MathJax -->
            <script type="text/x-mathjax-config">
            MathJax.Hub.Config({
              tex2jax: {inlineMath: [['$$$','$$$']], displayMath: [['$$$$$$','$$$$$$']]}
            });
            </script>
            <script type="text/javascript" async
                    src="https://assets.codeforces.com/mathjax/MathJax.js?config=TeX-MML-AM_CHTML">
            </script>
            <!-- /MathJax -->
        """
        mathjax_url = 'https://assets.codeforces.com/mathjax/MathJax.js'
        new_mathjax_url = self.image_func(mathjax_url, self.oj_name)
        self.append_html = self.append_html.replace(mathjax_url, new_mathjax_url)

    @property
    def browser(self):
        return self.rb

    @property
    def url_home(self):
        return 'http://codeforces.com/'

    def url_problem(self, cid: int, pid: str):
        # codeforces需要一个cid和一个pid来确定题目
        return self.url_home + 'problemset/problem/{}/{}'.format(cid, pid)

    @property
    def url_login(self):
        return self.url_home + 'enter/'

    @property
    def url_submit(self):
        return self.url_home + 'problemset/submit/'

    @property
    def url_status(self):
        return self.url_home + 'problemset/status/'

    @property
    def http_headers(self):
        return {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Ubuntu Chromium/52.0.2743.116 Chrome/52.0.2743.116 Safari/537.36',
            'Origin': "http://codeforces.com",
            'Host': "codeforces.com",
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
        }

    @property
    def uncertain_result_status(self):
        # 注意这里不是完全相等而是in
        return ['running', 'in queue']

    def get(self, url):
        try:
            self.browser.open(url, timeout=HTTP_METHOD_TIMEOUT)
            return self.browser.url == url
        except (HTTPError, URLError) as error:
            logger.error('Data not retrieved because %s\nURL: %s', error, url)
            return None
        except timeout:
            logger.error('socket timed out\nURL: %s', url)
            return None

    def post(self, url, data):
        try:
            return self.browser.open(url, 'post', data=data, timeout=HTTP_METHOD_TIMEOUT)
        except (HTTPError, URLError) as error:
            logger.error('Data not retrieved because %s\nURL: %s', error, url)
            return None
        except timeout:
            logger.error('socket timed out\nURL: %s', url)
            return None

    @staticmethod
    def get_languages():
        return {
            'GNU GCC 5.1.0': '10',
            'GNU GCC C11 5.1.0': '43',
            'Clang++17 Diagnostics': '52',
            'GNU G++ 5.1.0': '1',
            'GNU G++11 5.1.0': '42',
            'GNU G++14 6.4.0': '50',
            'GNU G++17 7.3.0': '54',
            'GNU C++17 Diagnostics (DrMemory)': '53',
            'Microsoft Visual C++ 2010': '2',
            'C# Mono 5': '9',
            'D DMD32 v2.079.0': '28',
            'Go 1.8': '32',
            'Haskell GHC 7.8.3': '12',
            'Java 1.8.0_162': '36',
            'Kotlin 1.2': '48',
            'OCaml 4.02.1': '19',
            'Delphi 7': '3',
            'Free Pascal 3': '4',
            'PascalABC.NET 2': '51',
            'Perl 5.20.1': '13',
            'PHP 7.0.12': '6',
            'Python 2.7': '7',
            'Python 3.6': '31',
            'PyPy 2.7 (6.0.0)': '40',
            'PyPy 3.5 (6.0.0)': '41',
            'Ruby 2.0.0p645': '8',
            'Rust 1.26': '49',
            'Scala 2.12': '20',
            'JavaScript V8 4.8.0': '34',
            'Node.js 6.9.1': '55',
            'ActiveTcl 8.5': '14',
            'Io-2008-01-07 (Win32)': '15',
            'Pike 7.8': '17',
            'Befunge': '18',
            'OpenCobol 1.0': '22',
            'Factor': '25',
            'Secret_171': '26',
            'Roco': '27',
            'Ada GNAT 4': '33',
            'Mysterious Language': '38',
            'FALSE': '39',
            'Picat 0.9': '44',
            'GNU C++11 5 ZIP': '45',
            'Java 8 ZIP': '46',
            'J': '47',
            'Microsoft Q#': '56',
        }

    def login(self):
        try:
            self.browser.open(self.url_login, timeout=HTTP_METHOD_TIMEOUT)
            enter_form = self.browser.get_form('enterForm')
            enter_form['handleOrEmail'] = self.handle
            enter_form['password'] = self.password
            self.browser.submit_form(enter_form)
            # checks = list(map(lambda x: x.getText()[1:].strip(),
            #                   self.browser.select('div.caption.titled')))
            if self.browser.url == self.url_home:
                return True, ''
            elif self.browser.url == self.url_login:
                # <span class="error for__password">
                soup = BeautifulSoup(self.browser.response.content, 'html5lib')
                return False, soup.find('span', {'class': 'error for__password'}).text
            else:
                return False, '登陆：未知错误'

        except (HTTPError, URLError) as error:
            return False, '登陆：HTTPError/URLError - ' + str(error)
        except timeout:
            return False, '登陆：http方法超时'

    def is_login(self):
        self.browser.open(self.url_home)
        checks = list(map(lambda x: x.getText()[1:].strip(),
                          self.browser.select('div.caption.titled')))
        return self.handle in checks

    def replace_image(self, html):
        # <img class="tex-graphics" src="/predownloaded/e6/1a/e61a341f8b20d0e351ba708597ce43b451f51e25.png"
        # style="max-width: 100.0%;max-height: 100.0%;">
        pos = html.find('<img')
        if pos == -1:
            return html
        src_pos = html[pos:].find('src=') + pos
        stp = src_pos + 5
        edp = html[stp:].find('"') + stp
        image_url = self.url_home[:-1] + html[stp:edp]
        saved_url = self.image_func(image_url, self.oj_name)
        return html[:stp] + saved_url + self.replace_image(html[edp:])

    def get_problem(self, cid, pid):
        ret = self.get(self.url_problem(cid, pid))

        if ret:
            soup = BeautifulSoup(self.browser.response.content, 'html5lib')
            header = soup.find('div', {'class': 'header'})
            title = header.find('div', {'class': 'title'}).text[len(pid) + 1:].strip()

            interactive = soup.find('span', {'class': 'tex-font-style-bf'})
            problem_type = 'interactive' \
                if (interactive and interactive.text == 'This is an interactive problem.') \
                else 'special judge'

            origin = self.url_problem(cid, pid)

            time_limit = {
                'default': int(float(header.find('div', {'class': 'time-limit'}).contents[1].split(' ')[0]) * 1000),
            }
            memory_limit = {
                'default': int(header.find('div', {'class': 'memory-limit'}).contents[1].split(' ')[0]) * 1024,
            }
            samples_input = []
            samples_output = []
            descriptions = []
            category = ''
            tags = []

            append_html = self.append_html

            htmls = header.find_next_siblings('div')
            for item in htmls:
                temp = item.find('div', {'class': 'section-title'})
                sub_title = temp.text if temp else ''
                sub_content = ''.join([str(item) for item in temp.find_next_siblings()])
                if sub_title == 'Example':
                    continue
                descriptions.append(
                    (sub_title, sub_content)
                )

            inputs = soup.find_all('div', {'class': 'input'})
            outputs = soup.find_all('div', {'class': 'output'})
            assert len(inputs) == len(outputs)
            n = len(inputs)
            for i in range(n):
                samples_input.append(inputs[i].text)
                samples_output.append(outputs[i].text)

            category = soup.find('a', {'style': 'color: black'}).text
            tag_htmls = soup.find_all('tag-box', {'style': 'font-size:1.2rem;'})
            for tag_html in tag_htmls:
                tags.append(tag_html.text)

            compatible_data = {}
            for key in self.compatible_problem_fields:
                compatible_data[key] = eval(key)
            return True, compatible_data

        elif ret is None:
            return False, '获取题目：http方法错误，请检查网络后重试'
        else:
            return False, '获取题目：不存在的题目'

    def submit_code(self, source, lang, cid, pid):
        if not self.is_login():
            success, info = self.login()
            if not success:
                return False, info

        problem_id = '{}{}'.format(cid, pid).upper()

        self.get(self.url_submit)
        submit_form = self.browser.get_form(class_='submit-form')
        submit_form['submittedProblemCode'] = problem_id
        submit_form['source'] = source
        # TODO: 把cf的语言全部转为大写
        submit_form['programTypeId'] = self.get_languages()[lang]
        self.browser.submit_form(submit_form)
        if self.browser.url == self.url_status[:-1]:
            ok, info = self.get_result()
            return (True, info['rid']) if ok else (False, '提交代码（获取提交id）：' + info)
        elif self.url_submit in self.browser.url:
            soup = BeautifulSoup(self.browser.response.content, 'html5lib')
            info = soup.find('span', {'class': 'error for__source'}).text
            return False, info
        else:
            return False, '提交代码：未知错误'



    def get_result(self):
        return True
# cf和poj或者hdu有所不同，不同题目可能有限制提交的语言
