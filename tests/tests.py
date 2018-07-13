# -*- coding: utf-8 -*-
# Created by crazyX on 2018/7/7
from crawlers.older.hdu import hdu_submit
from crawlers.older.poj import poj_submit
from crawlers.older.cf import cf_submit

import unittest


class Test(unittest.TestCase):
    def test_crawler_hdu(self):
        pid = 1000
        lang = 'g++'
        src = '''
        #include<bits/stdc++.h>
        using namespace std;
        int main()
        {
            int a,b;
            while(cin>>a>>b)cout<<a-b<<endl;
            return 0;
        }
        '''
        print(hdu_submit(pid, lang, src))

    def test_crawler_poj(self):
        pid = 1000
        lang = 'g++'
        src = '''
        #include<iostream>
        using namespace std;
        int main()
        {
            int a,b;
            while(cin>>a>>b)cout<<a-b<<endl;
            return 0;
        }
        '''
        print(poj_submit(pid, lang, src))

    def test_crawler_cf(self):
        pid = '1A'
        lang = 'g++'
        src = '''
        #include <iostream>
        using namespace std;
        int n,m,a;
        long long x,y;
        int main() {
            cin>>n>>m>>a;
            x=n/a+(n%a==0?0:1);
            y=m/a+(m%a==0?0:1);//sadjiowdqwdw
            cout<<x*y<<endl;
            return 0;
            //fuck you you
        }
        '''
        print(cf_submit(pid, lang, src))


if __name__ == '__main__':
    unittest.main()
