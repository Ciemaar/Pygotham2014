from holders import AbstractBaseHolder, BaseHolder

__author__ = 'andriod'

from itertools import chain
import Quandl


class QuandlAsset(object):
    def __init__(self, quandl_name, authtoken=None, **kwargs):
        """Uses the Quandl service to get live data

        :rtype : QuandlAsset
        :type quandl_name: str - an asset name assigned by Quandl
        :type authtoken: builtins.NoneType - Quandl auth token if available
        """
        self._authtoken = authtoken
        self.quandl_name = quandl_name
        self._value = None
        self.kwargs = kwargs

    def __getattr__(self, item):
        """Redirect any unknown attribute access to the data retrieved from Quandl, this constitutes a proxy
        """
        return getattr(self.value, item)

    def __getitem__(self, key):
        return self.value[key]

    def __len__(self):
        return len(self.value)

    @property
    def value(self):
        if self._value is not None:
            return self._value
        self._value = Quandl.get(self.quandl_name, authtoken=self._authtoken, **self.kwargs)
        return self._value


class QuandlHolder(AbstractBaseHolder):
    _instance_vars = AbstractBaseHolder._instance_vars + ['prefix','authtoken']
    def __init__(self, name_map_or_prefix, name, *prev_path, **kwargs):
        super(QuandlHolder, self).__init__(name, *prev_path)
        if isinstance(name_map_or_prefix, basestring):
            self.prefix = name_map_or_prefix
        else:
            self.name_map = name_map_or_prefix
        self.authtoken=None
        self.kwargs = kwargs

    def create_sub_obj(self, item):
        if getattr(self, 'prefix', None):
            return QuandlAsset(self.prefix+item, authtoken=self.authtoken, **self.kwargs)
        else:
            return QuandlAsset(self.name_map[item], authtoken=self.authtoken, **self.kwargs)


def get_live(sys_coll, model_coll, authtoken=None):
    coll = BaseHolder(sys_coll, "market")
    if hasattr(sys_coll, 'quandlFXCodes'):
        coll.fx = QuandlHolder(sys_coll.quandlFXCodes, "fx", (coll,), trim_start=model_coll.config.start_date)
    coll.stock = QuandlHolder('WIKI/', "stock", (coll,), trim_start=model_coll.config.start_date)
    return coll


def search_quandl(query, source="QUANDL", authtoken=None):
    currPage = True
    quandlAll = []
    pageNo = 0
    while currPage:
        currPage = Quandl.search(query, source=source, prints=False, page=pageNo, authtoken=authtoken)
        quandlAll.append(currPage)
        pageNo += 1
    return chain(*quandlAll)


def name_to_code(query='USD', source="QUANDL", authtoken=None):
    quandlAll = search_quandl(query, source=source, authtoken=authtoken)
    return {"%s_%s" % (curve['code'][7:10].lower(), curve['code'][10:].lower()): curve['code'] for curve in quandlAll}


def dl_quandl(query="USD", authtoken=None):
    count = 0
    for name, code in name_to_code(query=query, authtoken=authtoken).items():
        curve = Quandl.get(code, authtoken=authtoken)
        curve.to_csv(name + ".csv")
        count += 1
    print("Got %d curves" % count)


if __name__ == "__main__":
    test = QuandlAsset("GOOG/NYSE_ERO")
    print(test)
    print(test.value)
    print(test.Close['2009-05-14'])

    dl_quandl("USD")
    # dl_quandl("EUR")

