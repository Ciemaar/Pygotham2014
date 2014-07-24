from holders import AbstractBaseHolder, BaseHolder

__author__ = 'andriod'

from itertools import chain
import Quandl


class QuandlAsset(object):
    def __init__(self, quandl_name, authtoken=None):
        """Uses the Quandl service to get live data

        :type quandl_name: str - an asset name assigned by Quandl
        :type authtoken: builtins.NoneType - Quandl auth token if available
        """
        self._authtoken = authtoken
        self.quandl_name = quandl_name
        self._value = None

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
        self._value = Quandl.get(self.quandl_name, authtoken=self._authtoken)
        return self._value


class QuandlHolder(AbstractBaseHolder):
    def __init__(self, name_map, name, *prev_path):
        super(QuandlHolder, self).__init__(name, *prev_path)
        self.name_map = name_map

    def create_sub_obj(self, item):
        return QuandlAsset(self.name_map[item])


def get_live(sys_coll):
    coll = BaseHolder(sys_coll, "market")
    if hasattr(sys_coll,'quandlFXCodes'):
        coll.fx = QuandlHolder(sys_coll.quandlFXCodes, "fx", (coll,))
    return coll


def search_quandl(query, authtoken=None):
    currPage = True
    quandlAll = []
    pageNo = 0
    while currPage:
        currPage = Quandl.search(query, source="QUANDL", prints=False, page=pageNo, authtoken=authtoken)
        quandlAll.append(currPage)
        pageNo += 1
    return chain(*quandlAll)


def name_to_code(query='USD', authtoken=None):
    quandlAll = search_quandl(query, authtoken)
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

