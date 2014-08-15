import logging

log = logging.getLogger(__name__)
logging.basicConfig()

from pricing import price_holding
from data_access import get_file
from fund import FundsHolder
from quandl_streams import get_live
from simple_files import FileHolder

__author__ = 'andriod'

import unittest


class PricingCase(unittest.TestCase):
    def setUp(self):
        self.funds = FundsHolder('funds')
        self.model = FileHolder('model')
        self.market = get_live(get_file("sys"), self.model)

    def test_price(self):
        position_info = self.funds.rip.T[1]
        self.assertAlmostEqual(price_holding(position_info, self.market, self.model, '2014-03-03'), 447.2384)

    def test_price2(self):
        position_info = {'instrument_type': 'stock', 'end_date': None, 'instrument': 'SCI', 'cost': None,
                         'start_date': '2013-03-08', 'quantity': 23.84}
        self.assertAlmostEqual(price_holding(position_info, self.market, self.model, '2014-03-03'), 447.2384)

    def test_price_all(self):
        all_prices = sorted(fund.price(self.market, self.model, '2014-05-14') for fund in self.funds)
        self.assertEqual(len(all_prices), 10)
        print all_prices
        self.assertListEqual(all_prices, [20.224229000000001, 52.77375399999999, 54.362542000000019, 74.230075999999997,
                                          85.053227000000007, 96.373496000000017, 122.020098, 4099.5227000000004,
                                          4139.9243000000006, 59459.754800000002])


if __name__ == '__main__':
    unittest.main()
