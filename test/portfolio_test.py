import logging

log = logging.getLogger(__name__)
logging.basicConfig()

from data_access import get_file
from fund import FundsHolder
from portfolio import PortfoliosHolder
from quandl_streams import get_live
from simple_files import FileHolder

__author__ = 'Andy Fundinger - Andy.Fundinger@riskfocus.com'

import unittest


class PortfolioTestCase(unittest.TestCase):
    def setUp(self):
        self.portfolios = PortfoliosHolder('portfolio')
        self.funds = FundsHolder('funds')
        self.model = FileHolder('model')
        self.market = get_live(get_file("sys"), self.model)

    def test_price_all(self):
        all_prices = [portfolio.price(self.funds, self.market, self.model, '2014-05-14') for portfolio in
                      self.portfolios]
        assert len(all_prices) == 2
        self.assertListEqual(all_prices, [6170175.198071707, 6338728.6832171828])

    def test_hVar(self):
        portfolio = self.portfolios.scenario_1
        self.assertAlmostEqual(portfolio.hVar(self.funds, self.market, self.model, '2014-5-14'), 814564.40240158793)
        self.assertAlmostEqual(portfolio.hVar(self.funds, self.market, self.model, '2014-08-01'), 1418300.1873188419)


if __name__ == '__main__':
    unittest.main()
