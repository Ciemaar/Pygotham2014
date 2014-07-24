from abc import abstractmethod
from collections import MutableMapping
from warnings import warn

__author__ = 'andriod'


class AbstractBaseHolder(MutableMapping, object):
    next_type = None
    instance_vars = ['instance_vars', 'yaml_dict', 'next_type']

    def __init__(self, name, *prev_path):
        self.name = name
        self._cache = {}
        self.path = prev_path + (self,)

        if self.next_type is None:
            self.next_type = type(self)

    def __getitem__(self, item):
        """Overriding the [indexing] operation

        :type item: str - the key being accessed by [indexing]
        :return:
        """
        if item not in self._cache:
            ret = self.create_sub_obj(item)
            self._cache[item] = ret
        return self._cache[item]

    def __getattr__(self, item):
        """Overriding attribute access

        :type item: str - attribute requested
        :return: :raise AttributeError:
        """
        if item not in self.instance_vars and not item[0] == "_":
            return self[item]
        else:
            raise AttributeError

    @abstractmethod
    def create_sub_obj(self, item):
        pass

    def __repr__(self, *args, **kwargs):
        return "< {path} - {value} ".format(path=",".join(x.name for x in self.path), value=self.value)

    def __str__(self, *args, **kwargs):
        return str(self.value)

    def __iter__(self):
        return iter(self._cache)

    def __len__(self):
        return len(self._cache)

    def __delitem__(self, key):
        del self._cache[key]

    def __setitem__(self, key, value):
        self._cache[key] = value


class BaseHolder(AbstractBaseHolder):
    def create_sub_obj(self, item):
        warn("BaseHolders should never be called to create objects")
        return None