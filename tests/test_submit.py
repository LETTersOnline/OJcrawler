# -*- coding: utf-8 -*-
# Created by crazyX on 2018/7/7

from control import Controller

import unittest


class Test(unittest.TestCase):

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
        ctl = Controller('hdu', 'USTBVJ', 'USTBVJ')
        ctl.run(pid, ac_src, lang)
        ctl.run(pid, wa_src, lang)

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
            while(cin>>a>>b)cout<<a-b<<endl;
            return 0;
        }
        '''
        ctl = Controller('poj', 'USTBVJ', 'USTBVJ')
        ctl.run(pid, ac_src, lang)
        ctl.run(pid, wa_src, lang)

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


if __name__ == '__main__':
    unittest.main()
