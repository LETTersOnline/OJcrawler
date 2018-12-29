# -*- coding: utf-8 -*-
# Created by crazyX on 2018/7/7

from ojcrawler.control import Controller
import json
import unittest
import os

data = json.load(open(os.path.join(os.getcwd(), 'accounts.json')))

class Test(unittest.TestCase):

    def setUp(self):
        self.ctl = Controller()
        for oj_name in data:
            self.ctl.update_account(oj_name, data[oj_name]['handle'], data[oj_name]['password'])

    def test_submit(self):
        pass
        # self.crawler_hdu()
        # self.crawler_poj()
        # self.crawler_cf()

    def test_crawler_hdu(self):
        pid = 1000
        lang = 'g++'
        ac_src = '''
        #include<bits/stdc++.h>
        using namespace std;
        int main()
        {
            int a,b;
            while(cin>>a>>b)cout<<a+b<<endl;
            return 0;
        }
        '''
        wa_src = '''
        #include<bits/stdc++.h>
        using namespace std;
        int main()
        {
            int a,b;
            while(cin>>a>>b)cout<<a-b<<endl;
            return 0;
        }
        '''
        self.ctl.submit_code('hdu', ac_src, lang, pid)
        self.ctl.submit_code('hdu', wa_src, lang, pid)

    def test_crawler_poj(self):
        pid = 1000
        lang = 'g++'
        wa_src = '''
        #include<iostream>
        using namespace std;
        int main()
        {
            int a,b;
            while(cin>>a>>b)cout<<a-b<<endl;
            return 0;
        }
        '''
        ac_src = '''
        #include<iostream>
        using namespace std;
        int main()
        {
            int a,b;
            while(cin>>a>>b)cout<<a+b<<endl;
            return 0;
        }
        '''
        self.ctl.submit_code('poj', ac_src, lang, pid)
        self.ctl.submit_code('poj', wa_src, lang, pid)

    def test_crawler_cf(self):
        pid = '1A'
        lang = 'GNU G++11 5.1.0'
        src = '''
        #include <iostream>
        using namespace std;
        int n,m,a;
        long long x,y;
        hello ce
        int main() {
            cin>>n>>m>>a;
            x=n/a+(n%a==0?0:1);
            y=m/a+(m%a==0?0:1);
            cout<<x*y<<endl;
            return 0;
        }
        '''
        self.ctl.submit_code('codeforces', src, lang, pid)


if __name__ == '__main__':
    unittest.main()
