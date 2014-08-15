import logging

log = logging.getLogger(__name__)

from pandas import bdate_range
from fund import Fund

from simple_files import ObjectHolder


__author__ = 'Andy Fundinger - Andy.Fundinger@riskfocus.com'


class Portfolio(Fund):
    def price(self, funds, market, model, cob_date):
        """Price the portfolio by pricing all its funds and scaling

        :type funds: fund.FundsHolder
        :type market: holders.BaseHolder
        :type model: simple_files.FileHolder
        :type cob_date: str or date
        :return:
        """
        try:
            return self.components.apply(
                lambda component: component['quantity'] * funds[component['fund_name']].price(market, model, cob_date),
                axis=1).sum()
        except TypeError:
            log.warning("Unable to price on %s", cob_date)
            return None

    def hVar(self, funds, market, model, cob_date, days=262):
        """Calculate the historical var for this portfolio on the given date.

        :type funds: fund.FundsHolder fund coposition data
        :type market: holders.BaseHolder market data
        :type model: simple_files.FileHolder model data for use by pricers
        :type cob_date: str cob date to calculate var for
        :type days: int number of business days to look back for the historical market data, defaults to 262 which works
                    by pandas logic
        :return:
        """
        dates = bdate_range(end=cob_date, periods=days)
        log.info("Calculating hVar using date range [%s:%s]", dates[0].date(), dates[-1].date())
        prices = dates.to_series().apply(lambda dt: self.price(funds, market, model, dt.date()))
        return self.price(funds, market, model, cob_date) - prices.dropna().quantile(.05)


class PortfoliosHolder(ObjectHolder):
    klass = Portfolio
