# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from collections import OrderedDict
from .schema import MetaData


class TableData(OrderedDict):
    def __init__(self, name, dictlike):
        self.name = name
        super(TableData, self).__init__(dictlike)


def from_sqlalchemy_tables(tables, rule_set):
    metadata = MetaData()
    table_datas = []
    for table in tables:
        table_dic = OrderedDict()
        for col in table.columns:
            table_dic[col.name] = col

        table_data = TableData(table.name, table_dic)
        table_datas.append(table_data)

    rule_set.apply_all(metadata=metadata, tables=table_datas)
    return metadata