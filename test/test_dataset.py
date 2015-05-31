# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from . import sample

from testdatautil.rule import SqlAlchemyRuleSet
from testdatautil import dataset


def test_DataSet():
    tables = sample.BaseMaster.metadata.sorted_tables
    ruleset = SqlAlchemyRuleSet.create()
    metadata = dataset.from_sqlalchemy_tables(tables, ruleset)
    assert metadata._items
