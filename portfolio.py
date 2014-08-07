import os
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
        # ret = ret.T.append(pd.Series(ret.index.astype(str),ret.index, name='new_id')).T

        return Portfolio(ret)

    def __iter__(self):
        for key in os.listdir(self.file_path):
            key, _ = os.path.splitext(key)
            yield self[key]
