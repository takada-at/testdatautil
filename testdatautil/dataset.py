# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import testdata
from collections import OrderedDict
from .schema import BaseSchema, MetaData, Table, Column


file_template = """\
metadata = MetaData()

{classdefs}
"""

class_template = """\
from testdatautil.schema import BaseSchema, MetaData
from testdata import *


class {classname}(BaseSchema):
    __tablename__ = "{tablename}"
    _keys = {keys}

    metadata = metadata

{fielddefs}
"""

field_template = """\
    {name} = {definition}
"""


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
                args.append(Column(field_name, factory()))

            factory = Table(*args)
            tables[table_name] = factory

        self._metadata.tables = tables

    def evaluate_all(self):
        self._generators = self._rule_set.apply_all(self._tables)
        glob = dict(metadata=self._metadata, BaseSchema=BaseSchema)
        glob.update(vars(testdata))
        classdefs = []
        for table_name, table_data in self._tables.items():
            definition = self.generate_def(table_name, table_data)
            exec(definition, glob)
            classdefs.append(definition)

        self._code = file_template.format(classdefs="\n\n".join(classdefs))
        return glob

    def generate_def(self, table_name, table_data):
        fielddefs = []
        keys = []
        for field_name, _ in table_data.items():
            generator = self._generators[table_name][field_name]
            keys.append(field_name)
            fielddefs.append(field_template.format(
                name=field_name,
                definition=generator.generate()))

        class_name = "Factory_" + table_name
        classdef = class_template.format(classname=class_name,
                                         keys=repr(keys),
                                         tablename=table_name,
                                         fielddefs="\n".join(fielddefs))
        return classdef


def from_sqlalchemy_tables(tables, rule_set):
    metadata = MetaData()
    datasets = DataSet(metadata=metadata, rule_set=rule_set)
    for table in tables:
        for col in table.columns:
            datasets.add_item(table.name, col.name, col)

    #datasets.evaluate_all()
    datasets.create_all()
    return metadata