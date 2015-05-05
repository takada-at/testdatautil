# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import os
import shutil
import tempfile
from test import sample
from testdatautil.cli import execute_from_command_line
from testdatautil.rule import SqlAlchemyRuleSet
from testdatautil.dataset import from_sqlalchemy_tables


class MyRule(SqlAlchemyRuleSet):
    @classmethod
    def create(cls):
        rule = SqlAlchemyRuleSet.create()
        return rule


def test_cli():
    dirname = tempfile.mkdtemp()
    rule = MyRule.create()
    testdatameta = from_sqlalchemy_tables(sample.BaseMaster.metadata.sorted_tables,
                                          rule_set=rule)
    argv = ["-o{}".format(dirname)]
    execute_from_command_line(metadata=testdatameta, argv=argv)
    filename = os.path.join(dirname, "m_area.csv")
    assert os.path.exists(filename)
    shutil.rmtree(dirname)