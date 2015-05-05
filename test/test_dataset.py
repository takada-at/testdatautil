# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from . import sample

from testdatautil.rule import SqlAlchemyRuleSet
from testdatautil import dataset
from testdatautil.schema import MetaData


def test_DataSet():
    metadata = MetaData()
    tables = sample.BaseMaster.metadata.sorted_tables
    ruleset = SqlAlchemyRuleSet.create()
    dataset0 = dataset.DataSet(ruleset, metadata=metadata)
    for table in tables:
        for col in table.columns:
            dataset0.add_item(table.name, col.name, col)

    dataset0.create_all()
    assert metadata._items