from data_access import get_dummy

__author__ = 'andriod'

import unittest


class CoreTestCase(unittest.TestCase):
    def test_basics(self):
        print(repr(get_dummy("test")))


if __name__ == '__main__':
    unittest.main()
