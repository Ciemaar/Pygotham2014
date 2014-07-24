from collections import MutableMapping
import os

import pandas
import yaml


__author__ = 'andriod'


class FileHolder(MutableMapping, object):
    next_type = None

    def __init__(self, name, *prev_path):
        """FileHolders hold a section of the data and are matched in the file system with a matching directory or file

        :type name: str - name of the file or directory corresponding to this instance
        :param prev_path: - tuple of the FileHolders in the to this point
        """
        self.name = name
        self.path = prev_path + (self,)
        self.is_dir = os.path.isdir(self.file_path)
        self._yaml_obj = None

        self._cache = {}
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
        if item not in ['yaml_dict', 'file_path'] and not item[0] == "_":
            return self[item]
        else:
            raise AttributeError

    def create_sub_obj(self, item):
        """In both cases of .attribute and [indexing] we actually just continue to walk the tree

        :type item: str - the name of the next object
        :return: a newly created object, caller is responsible for caching
        """
        if self.yaml_obj:
            return self.yaml_obj[item]
        elif os.path.isfile(os.path.join(self.file_path, item) + ".csv"):
            return pandas.DataFrame.from_csv(os.path.join(self.file_path, item) + ".csv")
        return self.next_type(item, *self.path)

    @property
    def yaml_obj(self):
        if self._yaml_obj is not None:
            return self._yaml_obj
        elif os.path.isfile(self.file_path + ".yaml"):
            self._yaml_obj = yaml.load(open(self.file_path + ".yaml"))
            return self._yaml_obj
        else:
            return None

    @property
    def file_path(self):
        return str(os.path.join(*[x.name for x in self.path]))

    @property
    def value(self):
        if self.is_dir:
            return "Directory, no value"
        elif os.path.isfile(self.file_path):
            return open(self.file_path).read()
        elif os.path.isfile(self.file_path + ".yaml"):
            return yaml.load(open(self.file_path + ".yaml"))

    def __repr__(self, *args, **kwargs):
        return "< {path} - {value} ".format(path=",".join(x.name for x in self.path), value=self.value)

    def __str__(self, *args, **kwargs):
        return str(self.value)

    def __iter__(self):
        if self.is_dir:
            return (self[os.path.splitext(os.path.basename(path))[0]] for path in os.listdir(self.file_path))
        elif self.yaml_obj is not None:
            return iter(self.yaml_obj)
        else:
            return iter([]) #empty iter, we have no case for this now


    def __len__(self):
        if self.is_dir:
            return len(os.listdir(self.file_path))
        elif self.yaml_obj is not None:
            return len(self.yaml_obj)
        else:
            return 0  #empty iter, we have no case for this now

    def __delitem__(self, key):
        del self._cache[key]

    def __setitem__(self, key, value):
        self._cache[key] = value