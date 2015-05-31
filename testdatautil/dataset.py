# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from collections import (OrderedDict, namedtuple)
from .schema import MetaData


def create_dummy_model(table_name, table_dict):
    keys = table_dict.keys()
    model_name = table_name + 'Model'
    return namedtuple(model_name, keys)


class TableData(OrderedDict):
    def __init__(self, name, dictlike, model_class=None):
        self.name = name
        if model_class is None:
            model_class = create_dummy_model(name, dictlike)
        self.model_class = model_class
        super(TableData, self).__init__(dictlike)


def from_sqlalchemy_models(models, rule_set):
    metadata = MetaData()
    table_datas = []
    for model in models:
        table = model.__table__
        table_dic = OrderedDict()
        for col in table.columns:
            table_dic[col.name] = col

        table_data = TableData(table.name, table_dic,
                               model_class=model)
        table_datas.append(table_data)

    rule_set.apply_all(metadata=metadata, tables=table_datas)
    return metadata


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
