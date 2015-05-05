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
        classname = 'Factory_' + table.name
        for col in table.columns:
            dataset0.add_item(table.name, col.name, col)

    data = dataset0.evaluate_all()
    assert "Factory_m_area" in data
    cls = data['Factory_m_area']
    assert cls.metadata is metadata
    assert metadata._items