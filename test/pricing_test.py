import logging

log = logging.getLogger(__name__)
logging.basicConfig()

from pricing import price_holding
from data_access import get_file
from fund import FundsHolder
from quandl_streams import get_live
from simple_files import FileHolder

__author__ = 'Andy Fundinger - Andy.Fundinger@riskfocus.com'

import unittest


class PricingTestCase(unittest.TestCase):
    def setUp(self):
        self.funds = FundsHolder('funds')
        self.model = FileHolder('model')
        self.market = get_live(get_file("sys"), self.model)
    def test_price(self):
        """Test pricing by submitting a constructed dictionary for pricing"""
        position_info = {'instrument_type': 'stock', 'end_date': None, 'instrument': 'SCI', 'cost': None,
                         'start_date': '2013-03-08', 'quantity': 23.84}
        self.assertAlmostEqual(price_holding(position_info, self.market, self.model, '2014-03-03'), 443.6309848)

    def test_price2(self):
        """Same asset, but getting it from a fund instead"""
        position_info = self.funds.rip.T[1]
        self.assertAlmostEqual(price_holding(position_info, self.market, self.model, '2014-03-03'), 443.6309848)

    def test_price_all(self):
        """Test pricing of all funds

        Note:  This test is likely to hit rate limits in Quandl if run with a fully empty cache"""
        all_prices = sorted(fund.price(self.market, self.model, '2014-05-14') for fund in self.funds)
        self.assertEqual(len(all_prices), 10)
        print all_prices
        self.assertListEqual(all_prices,
                             [20.148345989692835, 32.735166499999998, 54.335754608853264, 74.204988516872945,
                              85.032083899177195, 96.228745868536876, 113.61060600100453, 4082.3602059991572,
                              4128.9950950721286, 8579.310249318105])


if __name__ == '__main__':
    unittest.main()
