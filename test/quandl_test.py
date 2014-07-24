import unittest

from data_access import get_file
from quandl_streams import get_live


__author__ = 'andriod'


class QuandlTestCase(unittest.TestCase):
    def test_market3(self):
        live_coll = get_live("market3", get_file("sys"))
        assert len(live_coll.fx['usd_eur'])
        assert live_coll.fx.usd_eur is live_coll.fx['usd_eur']


if __name__ == '__main__':
    unittest.main()
