import logging

log = logging.getLogger(__name__)

from quandl_streams import NoDataError
from Quandl.Quandl import DatasetNotFound, CallLimitExceeded

__author__ = 'Andy Fundinger - Andy.Fundinger@riskfocus.com'

pricers = {}

def pricer(func):
    """Decorator to register a pricer function

    :param func: a pricer function named xxx_yyy where yyy is the instrument_type to price, xxx is ignored
    :return: the same pricer function
    """
    global pricers
    _, name = func.__name__.split('_')
    pricers[name] = func
    return func

@pricer
def price_fx(holding, market, model, cob_date):
    """Price a foreign currency holding

    :type holding: pandas.core.series.Series
    :type market: holders.BaseHolder
    :type model: simple_files.FileHolder
    :type cob_date: str or date
    :return:
    """
    return holding['quantity'] / market.fx['_'.join((model.config['base_ccy'], holding['instrument']))].Rate[cob_date]

@pricer
def price_stock(holding, market, model, cob_date):
    """price a stock holding

    :type holding: pandas.core.series.Series
    :type market: holders.BaseHolder
    :type model: simple_files.FileHolder
    :type cob_date: str or date
    :return:
    """
    return (market.stock[holding['instrument']])['Adj. Close'][cob_date] * holding['quantity']

def price_holding(holding_info, market, model, cob_date):
    """General function to take a position and price it

    :type holding_info: pandas.core.series.Series
    :type market: holders.BaseHolder
    :type model: simple_files.FileHolder
    :type cob_date: str or date
    :return:
    """
    try:
        return pricers[holding_info['instrument_type']](holding_info, market, model, cob_date)
    except KeyError:
        log.warning("%s holding %s has no data for %s", holding_info['instrument_type'], holding_info['instrument'],
                    cob_date)
        raise

    # for any case of known, missing data errors from Quandl log it and return a 0 price
    except (NoDataError, DatasetNotFound, CallLimitExceeded):
        log.exception("Skipping position %s %s:%s", holding_info.name, holding_info['instrument_type'],
                      holding_info['instrument'])
    return 0


