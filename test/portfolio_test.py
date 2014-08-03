from data_access import get_file
from quandl_streams import get_live
from simple_files import FileHolder

__author__ = 'andriod'

import unittest


class PortfolioTestCase(unittest.TestCase):


    def setUp(self):
        self.portfolio = FileHolder('portfolio')
        self.model = FileHolder('model')
        self.market = get_live(get_file("sys"), self.model)

    def test_portfolio_access(self):
        assert len(self.portfolio.retirement)

    def test_cost(self):
        assert self.portfolio.retirement.cost.sum() == 200

    def test_price(self):
        value = 0
        for name, row in self.portfolio.retirement.iterrows():
            if row['instrument_type'] == 'fx':
                spot_rate = self.market.fx['_'.join((self.model.config['base_ccy'], row['instrument']))].Rate['2010-5-14']
            elif row['instrument_type'] == 'stock':
                spot_rate = (self.market.stock[row['instrument']]).Close['2010-5-14']
            value += spot_rate*row['quantity']
        self.assertAlmostEqual(value, 25461.2615)


if __name__ == '__main__':
    unittest.main()
