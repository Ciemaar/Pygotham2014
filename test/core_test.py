import logging

log = logging.getLogger(__name__)
logging.basicConfig()

from data_access import get_dummy

__author__ = 'Andy Fundinger - Andy.Fundinger@riskfocus.com'

import unittest


class CoreTestCase(unittest.TestCase):
    def test_basics(self):
        print(repr(get_dummy("test")))


if __name__ == '__main__':
    unittest.main()
