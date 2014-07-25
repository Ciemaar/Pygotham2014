from simple_files import FileHolder

__author__ = 'andriod'

import unittest


class PortfolioTestCase(unittest.TestCase):


    def setUp(self):
        self.portfolio = FileHolder('portfolio')

    def test_portfolio_access(self):
        assert len(self.portfolio.retirement)

    def test_cost(self):
        assert self.portfolio.retirement.cost.sum() == 100

if __name__ == '__main__':
    unittest.main()
