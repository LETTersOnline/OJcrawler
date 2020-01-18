import unittest

from ojcrawler.control import Controller


class TestCrawlContest(unittest.TestCase):

    def test_something(self):
        controller = Controller()
        results = controller.get_contest('codeforces', 1221)
        self.assertEqual(
            results,
            ['x5281', 'x3781', 'x4455', 'x1309', 'x112', 'x78', 'x9'],
            results)


if __name__ == '__main__':
    unittest.main()
