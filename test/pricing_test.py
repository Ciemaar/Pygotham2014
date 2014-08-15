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
        self.assertListEqual(all_prices, sorted(
            [4139.9243000000006, 85.053227000000007, 4099.5227000000004, 122.020098, 96.709960000000024,
             59459.754800000002]))


if __name__ == '__main__':
    unittest.main()
