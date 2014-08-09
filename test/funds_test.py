from pandas import date_range

from data_access import get_file
from fund import FundsHolder
from pricing import price_fund
from quandl_streams import get_live
from simple_files import FileHolder


__author__ = 'andriod'

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
        value = price_fund(self.funds.retirement, self.market, self.model, '2010-5-14')
        self.assertAlmostEqual(value, 25461.2615)
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
                print "unable to price for %s" % sample_date
        self.assertEquals(len(price_curve), 1321)


if __name__ == '__main__':
    unittest.main()
