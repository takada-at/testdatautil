# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import os
import sys
sys.path.append(
    os.path.join(os.path.dirname(__file__),
                 '..')
)
from testdatautil.cli import execute_from_command_line
from testdatautil.rule import SqlAlchemyRuleSet, SADateTime
from testdatautil.dataset import from_sqlalchemy_tables
from pkg import db


class StartTime(SqlAlchemyRuleSet):
    def match(self, rules, field, table_data, context):
        return field.name == 'starttime'


class MyRuleSet(SqlAlchemyRuleSet):
    @classmethod
    def create(cls):
        rule = SqlAlchemyRuleSet.create()
        return rule


def main():
    rule = MyRuleSet.create()
    testdatameta = from_sqlalchemy_tables(db.BaseMaster.metadata.sorted_tables,
                                          rule_set=rule)
    execute_from_command_line(metadata=testdatameta)


if __name__ == '__main__':
    main()