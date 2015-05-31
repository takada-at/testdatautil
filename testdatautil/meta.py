# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from sqlalchemy.schema import Table, MetaData
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy.ext.declarative import api


default_class_registry = {}

default_metadata = MetaData()


class Meta(DeclarativeMeta):
    _classcache = {}

    def __init__(cls, classname, bases, dict_):
        type.__init__(cls, classname, bases, dict_)


DefaultBase = Meta()


class ClassBuilder(object):
    @classmethod
    def get_class(cls, table_name):
        if table_name in cls._classcache:
            return cls._classcache[table_name]

        return cls._gen_master_class(table_name)

    @classmethod
    def _gen_class(cls, engine, table_name,
                   base_class=None, metadata=None,
                   class_registry=None):
        if base_class is None:
            base_class = DefaultBase
        if metadata is None:
            metadata = default_metadata
        if class_registry is None:
            class_registry = default_class_registry

        tableobj = Table(table_name, metadata, autoload=True,
                         autoload_with=engine)
        classname = 'Gen_' + table_name
        klass = cls(str(classname), (base_class,), {})
        klass.__tablename__ = table_name
        klass.__table__ = tableobj
        for c in tableobj.columns:
            setattr(klass, c.name, c)

        api.instrument_declarative(klass, class_registry, metadata)
        cls._classcache[table_name] = klass
        return klass

