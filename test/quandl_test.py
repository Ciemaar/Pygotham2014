import unittest

from data_access import get_file
from quandl_streams import get_live, QuandlAsset


__author__ = 'andriod'


class QuandlTestCase(unittest.TestCase):
    def test_market(self):
        live_coll = get_live(get_file("sys"))
        usdEurAsset = live_coll.fx['usd_eur']
        assert isinstance(usdEurAsset, QuandlAsset)
        assert len(usdEurAsset)
        assert live_coll.fx.usd_eur is usdEurAsset


if __name__ == '__main__':
    unittest.main()
