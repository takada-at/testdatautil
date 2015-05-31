# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import os
import sys
sys.path.append(
    os.path.join(os.path.dirname(__file__),
                 '..')
)
from datetime import datetime, timedelta
from testdatautil import cli
from testdatautil import dataset
from testdatautil.factory import DateIntervalFactory
from testdatautil.rule import SqlAlchemyRuleSet, SAFieldNameRule
from pkg import db


class StartDate(SAFieldNameRule):
    fieldname = 'startdate'

    def build(self, field):
        fromdate = (datetime.now() - timedelta(days=120)).date()
        return DateIntervalFactory(base=fromdate, delta=timedelta(days=1))


class StartTime(SAFieldNameRule):
    fieldname = 'starttime'

    def build(self, field):
        fromdate = datetime.now() - timedelta(days=120, minutes=20)
        return DateIntervalFactory(base=fromdate, delta=timedelta(days=1))


class EndTime(SAFieldNameRule):
    fieldname = 'endtime'

    def build(self, field):
        fromdate = datetime.now() - timedelta(days=120)
        return DateIntervalFactory(base=fromdate, delta=timedelta(seconds=220))


class MyRuleSet(SqlAlchemyRuleSet):
    @classmethod
    def create(cls):
        rule = SqlAlchemyRuleSet.create()
        rule.add_rule(StartTime())
        rule.add_rule(EndTime())
        rule.add_rule(StartDate())
        return rule


def main():
    rule = MyRuleSet.create()
    class_registry = db.BaseMaster._decl_class_registry
    models = [model for model in class_registry.values()
              if isinstance(model, type) and issubclass(model, db.BaseMaster)]
    testdatameta = dataset.from_sqlalchemy_models(models,
                                                  rule_set=rule)
    cli.execute_from_command_line(metadata=testdatameta)


if __name__ == '__main__':
    main()