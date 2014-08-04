from pricing import price_fund
from simple_files import FileHolder

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

    def price(self, market, model, cob_date):
        return price_fund(self.components, market, model, cob_date)


class PortfolioHolder(FileHolder):
    def create_sub_obj(self, item):
        ret = super(PortfolioHolder, self).create_sub_obj(item)
        return Portfolio(ret)