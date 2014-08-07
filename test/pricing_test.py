from data_access import get_file
from portfolio import PortfolioHolder
from quandl_streams import get_live
from simple_files import FileHolder

__author__ = 'andriod'

import unittest


class PricingCase(unittest.TestCase):
    def setUp(self):
        self.portfolio = PortfolioHolder('portfolio')
        self.model = FileHolder('model')
        self.market = get_live(get_file("sys"), self.model)

    def test_price_all(self):
        all_prices = [fund.price(self.market, self.model,'2014-05-14') for fund in self.portfolio]
        assert len(all_prices) == 3
        self.assertListEqual(all_prices,[4139.9243000000006, 4099.5227000000004, 59459.754800000002])



if __name__ == '__main__':
    unittest.main()
