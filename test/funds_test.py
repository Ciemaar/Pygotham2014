import logging

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

from pandas import date_range

from data_access import get_file
from fund import FundsHolder
from quandl_streams import get_live
from simple_files import FileHolder


__author__ = 'Andy Fundinger - Andy.Fundinger@riskfocus.com'

import unittest


class FundsTestCase(unittest.TestCase):
    def setUp(self):
        self.funds = FundsHolder('funds')
        self.model = FileHolder('model')
        self.market = get_live(get_file("sys"), self.model)

    def test_fund_access(self):
        assert len(self.funds.retirement) == 2

    def test_cost(self):
        assert self.funds.retirement.cost.sum() == 200

    def test_price(self):
        self.assertAlmostEqual(self.funds.retirement.price(self.market, self.model, '2010-5-14'), 25461.2615)

    def test_start_date(self):
        min_date = self.funds.retirement.start_date
        assert min_date == '2009-5-2'

    def test_price_curve(self):
        price_curve = []
        for sample_date in date_range(self.funds.retirement.start_date, '2014-08-01'):
            if sample_date.dayofweek >= 5:
                continue
            try:
                price_curve.append(
                    (sample_date, self.funds.retirement.price(self.market, self.model, sample_date.date())))
            except KeyError:
                print "unable to price for %s" % sample_date.date()
        self.assertEquals(sum(1 for date, price in price_curve if price is not None), 1370)

    def test_hVar(self):
        self.assertAlmostEqual(self.funds.retirement.hVar(self.market, self.model, '2010-5-14'), 11829.95528)
        self.assertAlmostEqual(self.funds.retirement.hVar(self.market, self.model, '2014-08-01'), 303.03944)


if __name__ == '__main__':
    unittest.main()
