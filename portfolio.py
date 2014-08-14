import os

from simple_files import ObjectHolder


__author__ = 'andriod'


class Portfolio(object):
    def __init__(self, components):
        super(Portfolio, self).__init__()
        self.components = components

    def __getattr__(self, item):
        """Redirect any unknown attribute access to the data retrieved from Quandl, this constitutes a proxy
        """
        return getattr(self.components, item)

    def __getitem__(self, key):
        return self.components[key]

    def __len__(self):
        return len(self.components)

    @property
    def start_date(self):
        return self.components['start_date'].min()

    def price(self, funds, market, model, cob_date):
        return self.components.apply(lambda component:component['quantity']*funds[component['fund_name']].price(market, model, cob_date), axis=1).sum()


class PortfoliosHolder(ObjectHolder):
    klass=Portfolio
