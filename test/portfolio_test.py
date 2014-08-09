from data_access import get_file
from fund import FundsHolder
from portfolio import PortfoliosHolder
from quandl_streams import get_live
from simple_files import FileHolder

__author__ = 'andriod'

import unittest


class PortfolioTestCase(unittest.TestCase):
    def setUp(self):
        self.portfolios = PortfoliosHolder('portfolio')
        self.funds = FundsHolder('funds')
        self.model = FileHolder('model')
        self.market = get_live(get_file("sys"), self.model)
        
    def test_price_all(self):
        all_prices = [portfolio.price(self.funds, self.market, self.model, '2014-05-14') for portfolio in self.portfolios]
        assert len(all_prices) == 1
        self.assertListEqual(all_prices, [6189685.6500000013])


if __name__ == '__main__':
    unittest.main()
