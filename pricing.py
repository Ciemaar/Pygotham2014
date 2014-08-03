from decimal import Decimal
from string import split

__author__ = 'andriod'

pricers = {}

def pricer(func):
    global  pricers
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
    return sum(pricers[row['instrument_type']](row, market, model, cob_date) for name, row in fund.iterrows())