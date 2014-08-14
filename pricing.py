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


def price_holding(holding_info, market, model, cob_date):
    # if row['position_id'][0] == '#':
    # continue
    try:
        return pricers[holding_info['instrument_type']](holding_info, market, model, cob_date)
    except NoDataError:
        log.exception("Skipping position %s %s:%s", holding_info.name, holding_info['instrument_type'], holding_info['instrument'])
    except DatasetNotFound:
        log.exception("Skipping position %s %s:%s", holding_info.name, holding_info['instrument_type'], holding_info['instrument'])
    except CallLimitExceeded:
        log.exception("Skipping position %s %s:%s", holding_info.name, holding_info['instrument_type'], holding_info['instrument'])
    return 0


