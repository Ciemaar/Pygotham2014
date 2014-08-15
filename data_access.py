from dingus import Dingus

from quandl_streams import get_live
from simple_files import FileHolder


__author__ = 'Andy Fundinger - Andy.Fundinger@riskfocus.com'


def get_dummy(coll_name):
    return Dingus("{coll_name}_env".format(coll_name=coll_name))


def get_file(coll_name):
    return FileHolder(coll_name)


if __name__ == "__main__":
    print(repr(get_dummy("test")))

    dummyCollection = get_dummy("market1")
    print(repr(dummyCollection))
    print(repr(dummyCollection.news))
    print(repr(dummyCollection.news['IBM']))
    print(repr(dummyCollection.news['IBM']['5-14-2010']))

    print(repr(dummyCollection.fx.usd_eur['High (est)']['2010-05-14']))
    print(repr(dummyCollection.fx.usd_eur['Low (est)']['2010-05-14']))
    print(repr(dummyCollection.fx.usd_eur.Rate['2010-05-14']))

    fileCollection = get_file("market1")
    print(repr(fileCollection))
    print(repr(fileCollection.news))
    print(repr(fileCollection.news['IBM']))
    print(repr(fileCollection.news['IBM']['5-14-2010']))

    liveCollection = get_live(get_file("sys"))
    print(repr(liveCollection.fx.usd_eur['High (est)']['2010-05-14']))
    print(repr(liveCollection.fx.usd_eur['Low (est)']['2010-05-14']))
    print(repr(liveCollection.fx.usd_eur.Rate['2010-05-14']))
