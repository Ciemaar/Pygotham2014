import logging
log = logging.getLogger(__name__)

from quandl_streams import NoDataError
from Quandl.Quandl import DatasetNotFound, CallLimitExceeded

__author__ = 'andriod'

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
    return market.fx['_'.join((model.config['base_ccy'], holding['instrument']))].Rate[cob_date] * holding['quantity']


@pricer
def price_stock(holding, market, model, cob_date):
    return (market.stock[holding['instrument']]).Close[cob_date] * holding['quantity']


def price_fund(fund, market, model, cob_date):
    ret = 0
    for name, row in fund.iterrows():
        # if row['position_id'][0] == '#':
        # continue
        try:
            ret += pricers[row['instrument_type']](row, market, model, cob_date)
        except NoDataError:
            log.exception("Skipping position %s %s:%s", name, row['instrument_type'], row['instrument'])
        except DatasetNotFound:
            log.exception("Skipping position %s %s:%s", name, row['instrument_type'], row['instrument'])
        except CallLimitExceeded:
            log.exception("Skipping position %s %s:%s", name, row['instrument_type'], row['instrument'])

    return ret