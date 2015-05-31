# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from collections import OrderedDict
from factory.base import (FactoryMetaClass, Factory)


class MetaData(object):
    def __init__(self):
        self._items = dict()

    def add(self, name, item):
        self._items[name] = item

    @property
    def tables(self):
        return self._items

    @tables.setter
    def tables(self, tabledata):
        self._items = tabledata

    def items(self):
        return self._items.items()


class Table(object):
    def __init__(self, name, model_class,
                 metadata, *columns):
        self.name = name
        self.model_class = model_class
        self.metadata = metadata
        self.columns = columns
        keys = []
        self._dic = OrderedDict()
        for col in self.columns:
            keys.append(col.name)
            self._dic[col.name] = col

        self._keys = keys

    def __getitem__(self, item):
        return self._dic[item]

    def keys(self):
        return self._keys

    def convert_to_factory(self, **kwargs):
        params = dict(kwargs)
        params['model'] = self.model_class
        metaclass = type("Meta", None, params)
        factory_params = dict(Meta=metaclass)
        for key in self.keys():
            factory_params[key] = getattr(self, key).factory

        class_name = "{}Factory".format(model.__name__)
        return FactoryMetaClass(class_name, (Factory,), factory_params)


class Column(object):
    def __init__(self, name, factory):
        self.name = name
        self.factory = factory