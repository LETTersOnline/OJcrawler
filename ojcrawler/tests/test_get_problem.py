from __future__ import print_function
from ojcrawler.control import Controller

if __name__ == '__main__':
    x = Controller()
    _, info = x.get_problem('hdu', '4114')
    print(_, info)
    _, info = x.get_problem('poj', '2114')
    print(_, info)
    _, info = x.get_problem('codeforces', '100a')
    print(_, info)



