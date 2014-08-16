import logging
from pandas import DataFrame
import sys

from data_access import get_file
from fund import FundsHolder
from portfolio import PortfoliosHolder
from quandl_streams import get_live
from simple_files import FileHolder


__author__ = 'Andy Fundinger - Andy.Fundinger@riskfocus.com'

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    cob_date = sys.argv[1]

    portfolios = PortfoliosHolder('portfolio')
    funds = FundsHolder('funds')
    model = FileHolder('model')
    results = FileHolder('results')
    market = get_live(get_file("sys"), model)

    risk_by_fund = DataFrame(
        ((fund.name, fund.price(market, model, cob_date), fund.hVar(market, model, cob_date)) for fund in funds),
        columns=['fund_name', 'price', 'hVar'])
    risk_by_fund['normalized_hVar'] = risk_by_fund['hVar'] / risk_by_fund['price']

    results['risk_by_fund'] = risk_by_fund

    risk_by_portfolio = DataFrame(((portfolio.name, portfolio.price(funds, market, model, cob_date),
                                    portfolio.hVar(funds, market, model, cob_date)) for portfolio in portfolios),
                                  columns=['portfolio_name', 'price', 'hVar'])
    risk_by_portfolio['normalized_hVar'] = risk_by_portfolio['hVar'] / risk_by_portfolio['price']

    results['risk_by_portfolio'] = risk_by_portfolio

    print risk_by_fund
    print risk_by_portfolio