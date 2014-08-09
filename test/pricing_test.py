import logging
log = logging.getLogger(__name__)
logging.basicConfig()

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

    def test_price_all(self):
        all_prices = [fund.price(self.market, self.model, '2014-05-14') for fund in self.funds]
        self.assertEqual(len(all_prices), 6)
        self.assertListEqual(all_prices, [4139.9243000000006, 85.053227000000007,  4099.5227000000004,  122.020098,  96.709960000000024,  59459.754800000002])


if __name__ == '__main__':
    unittest.main()
