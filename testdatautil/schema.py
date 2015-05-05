# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from collections import OrderedDict
from testdata.base import Factory
from testdata.dictionary import DictFactory
from testdata.metaclasses import DictFactoryBuilder


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


def with_metaclass(meta, *bases):
    class metaclass(meta):
        __call__ = type.__call__
        __init__ = type.__init__
        def __new__(cls, name, this_bases, d):
            if this_bases is None:
                return type.__new__(cls, name, (), d)
            return meta(name, bases, d)
    return metaclass('temporary_class', None, {})


class Table(Factory):
    def __init__(self, name, metadata, *columns):
        self.name = name
        self.metadata = metadata
        self.columns = columns
        keys = []
        for col in self.columns:
            keys.append(col.name)

        self._keys = keys
        Factory.__init__(self)

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


class SchemaMetaClass(type):
    def __new__(cls, classname, bases, dic):
        ignore = set(["metadata"])
        cls_ = type.__new__(cls, classname, bases, dic)
        facdict = OrderedDict()
        for key, val in vars(cls_).items():
            if isinstance(val, Factory):
                facdict[key] = val

        if facdict:
            fcclassname = "_Factory_" + classname
            factory = DictFactoryBuilder(fcclassname, (DictFactory,), facdict)
            cls_.__factory_class__ = factory
            cls_.metadata.add(cls_.__tablename__, cls_)

        return cls_


class BaseSchema(with_metaclass(SchemaMetaClass, object)):
    metadata = MetaData()

    def __init__(self):
        self.__factory__ = self.__factory_class__()

    def keys(self):
        return self._keys

    def generate(self, count):
        for data in self.__factory__.generate(count):
            ordered = OrderedDict()
            for key in self._keys:
                ordered[key] = data[key]

            yield ordered