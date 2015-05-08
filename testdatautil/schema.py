# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from collections import OrderedDict
from testdata.base import Factory


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


class Table(Factory):
    def __init__(self, name, metadata, *columns):
        self.name = name
        self.metadata = metadata
        self.columns = columns
        keys = []
        self._dic = OrderedDict()
        for col in self.columns:
            keys.append(col.name)
            self._dic[col.name] = col

        self._keys = keys
        Factory.__init__(self)

    def __getitem__(self, item):
        return self._dic[item]

    def __iter__(self):
        columns = []
        for col in self.columns:
            columns.append(iter(col))

        return super(Table, self).__iter__()

    def keys(self):
        return self._keys

    def increase_index(self):
        super(Table, self).increase_index()
        for col in self.columns:
            col.increase_index()

    def set_element_amount(self, element_amount):
        for col in self.columns:
            col.set_element_amount(element_amount)

        super(Table, self).set_element_amount(element_amount)

    def __call__(self, *args, **kwargs):
        result = OrderedDict()
        for col in self.columns:
            result[col.name] = col()

        return result


class Column(Factory):
    def __init__(self, name, factory):
        self.name = name
        self.factory = factory
        Factory.__init__(self)

    def __iter__(self):
        self.factory = iter(self.factory)
        return super(Column, self).__iter__()

    def set_element_amount(self, element_amount):
        super(Column, self).set_element_amount(element_amount)
        self.factory.set_element_amount(element_amount)

    def increase_index(self):
        super(Column, self).increase_index()
        self.factory.increase_index()

    def __call__(self, *args, **kwargs):
        return self.factory()
