# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from collections import OrderedDict
from .schema import MetaData


class DataSet(object):
    def __init__(self, rule_set, metadata):
        self._rule_set = rule_set
        self._tables = OrderedDict()
        self._metadata = metadata
        self._code = None
        self._generators = OrderedDict()

    def add_item(self, table_name, field_name, field):
        key = table_name
        if key not in self._tables:
            self._tables[key] = OrderedDict()

        self._tables[key][field_name] = field

    def create_all(self):
        tables = self._rule_set.apply_all(self._metadata,
                                          self._tables)


def from_sqlalchemy_tables(tables, rule_set):
    metadata = MetaData()
    datasets = DataSet(metadata=metadata, rule_set=rule_set)
    for table in tables:
        for col in table.columns:
            datasets.add_item(table.name, col.name, col)

    datasets.create_all()
    return metadata