import os

import pandas
import yaml

from holders import AbstractBaseHolder


__author__ = 'andriod'


class FileHolder(AbstractBaseHolder):
    _instance_vars = ['_instance_vars', 'yaml_dict', 'file_path']

    def __init__(self, name, *prev_path):
        """FileHolders hold a section of the data and are matched in the file system with a matching directory or file

        :type name: str - name of the file or directory corresponding to this instance
        :param prev_path: - tuple of the FileHolders in the to this point
        """
        super(FileHolder, self).__init__(name, *prev_path)
        self.is_dir = os.path.isdir(self.file_path)
        self._yaml_obj = None

    def __len__(self):
        if self.is_dir:
            return len(os.listdir(self.file_path))
        elif self.yaml_obj is not None:
            return len(self.yaml_obj)
        else:
            return 0  # empty iter, we have no case for this now

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
    def value(self):
        if self.is_dir:
            return "Directory, no value"
        elif os.path.isfile(self.file_path):
            return open(self.file_path).read()
        elif os.path.isfile(self.file_path + ".yaml"):
            return yaml.load(open(self.file_path + ".yaml"))

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
    def file_path(self):
        return str(os.path.join(*[x.name for x in self.path]))


class ObjectHolder(FileHolder):
    "A file holder that wraps the stored object in class, also iterable"
    def create_sub_obj(self, item):
        ret = super(ObjectHolder, self).create_sub_obj(item)
        # ret = ret.T.append(pd.Series(ret.index.astype(str),ret.index, name='new_id')).T

        return self.klass(ret)

    def __iter__(self):
        """Object Holders can be iterated to work on the funds in sequence


        """
        for key in os.listdir(self.file_path):
            key, _ = os.path.splitext(key)
            yield self[key]