# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from collections import OrderedDict
from .schema import MetaData


class TableData(OrderedDict):
    def __init__(self, name, dictlike):
        self.name = name
        super(TableData, self).__init__(dictlike)


class DataSet(object):
    def __init__(self, rule_set, metadata):
        self._rule_set = rule_set
        self._metadata = metadata
        self._code = None
        self._generators = OrderedDict()

    def create_all(self, table_datas):
        tables = self._rule_set.apply_all(self._metadata,
                                          table_datas)


def from_sqlalchemy_tables(tables, rule_set):
    metadata = MetaData()
    datasets = DataSet(metadata=metadata, rule_set=rule_set)
    table_datas = []
    for table in tables:
        table_dic = OrderedDict()
        for col in table.columns:
            table_dic[col.name] = col

        table_data = TableData(table.name, table_dic)
        table_datas.append(table_data)

    datasets.create_all(table_datas)
    return metadata