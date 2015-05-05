# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from collections import OrderedDict
from .schema import Table, Column, MetaData


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
        tables = OrderedDict()
        self._generators = self._rule_set.apply_all(self._tables)
        for table_name, table_data in self._generators.items():
            args = [table_name, self._metadata]
            for field_name, factory in table_data.items():
                args.append(Column(field_name, factory))

            factory = Table(*args)
            tables[table_name] = factory

        self._metadata.tables = tables


def from_sqlalchemy_tables(tables, rule_set):
    metadata = MetaData()
    datasets = DataSet(metadata=metadata, rule_set=rule_set)
    for table in tables:
        for col in table.columns:
            datasets.add_item(table.name, col.name, col)

    #datasets.evaluate_all()
    datasets.create_all()
    return metadata