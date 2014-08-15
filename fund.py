import logging

log = logging.getLogger(__name__)

from pandas.tseries.index import bdate_range
from pricing import price_holding
from simple_files import ObjectHolder


__author__ = 'Andy Fundinger - Andy.Fundinger@riskfocus.com'


class Fund(object):
    def __init__(self, name, components):
        """Hold information about the composition of a fund.

        :type components: pandas.core.frame.DataFrame
        """
        super(Fund, self).__init__()
        self.name = name
        self.components = components

    def __getattr__(self, item):
        """Redirect any unknown attribute access to the components panda, this constitutes a proxy

        :type item: str
        """
        if item[0] != '_':
            return getattr(self.components, item)
        else:
            # Default behaviour
            raise AttributeError

    def __getitem__(self, key):
        """Redirect any unknown index to the components panda

        :param key:
        :return:
        """
        return self.components[key]

    def __len__(self):
        """Fund length is the number of included positions


        :return:
        """
        return len(self.components)

    @property
    def start_date(self):
        """Funds start on the date of the first position in the fund.


        :return:
        """
        return self['start_date'].min()

    def price(self, market, model, cob_date):
        """Price the fund by pricing all of its positions

        :type market: holders.BaseHolder
        :type model: holders.BaseHolder
        :type cob_date: str or date
        :return:
        """
        try:
            return self.components.apply(price_holding, 1, args=(market, model, cob_date)).sum()
        except KeyError:
            log.warning("Fund %s unable to price on %s", self.name, cob_date)
            return None

    def hVar(self, market, model, cob_date, days=262):
        """Calculate the historical var for this fund on the given date.

        :type market: holders.BaseHolder market data
        :type model: simple_files.FileHolder model data for use by pricers
        :type cob_date: str cob date to calculate var for
        :type days: int number of business days to look back for the historical market data, defaults to 262 which works
                    by pandas logic
        :return:
        """
        dates = bdate_range(end=cob_date, periods=days)
        log.info("Calculating hVar using date range [%s:%s]", dates[0].date(), dates[-1].date())
        prices = dates.to_series().apply(lambda dt: self.price(market, model, dt.date()))
        return self.price(market, model, cob_date) - prices.dropna().quantile(.05)


class FundsHolder(ObjectHolder):
    "A holder that constructs fund objects out of the data stored in this collection"
    klass = Fund



