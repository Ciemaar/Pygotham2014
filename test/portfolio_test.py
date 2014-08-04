from data_access import get_file
from portfolio import PortfolioHolder
from pricing import price_fund
from quandl_streams import get_live
from simple_files import FileHolder

__author__ = 'andriod'

import unittest


class PortfolioTestCase(unittest.TestCase):
    def setUp(self):
        self.portfolio = PortfolioHolder('portfolio')
        self.model = FileHolder('model')
        self.market = get_live(get_file("sys"), self.model)

    def test_portfolio_access(self):
        assert len(self.portfolio.retirement) == 2

    def test_cost(self):
        assert self.portfolio.retirement.cost.sum() == 200

    def test_price(self):
        value = price_fund(self.portfolio.retirement, self.market, self.model, '2010-5-14')
        self.assertAlmostEqual(value, 25461.2615)

    def test_start_date(self):
        min_date = self.portfolio.retirement.start_date
        assert min_date == '2009-5-2'

if __name__ == '__main__':
    unittest.main()
