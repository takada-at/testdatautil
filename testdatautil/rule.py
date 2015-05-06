# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from collections import OrderedDict
from datetime import datetime, date, timedelta
from testdata import (RandomInteger, Constant, RandomSelection,
                      RandomLengthStringFactory,
                      RandomDateFactory, RandomFloat,
                      DateIntervalFactory,
                      FakeDataFactory, CountingFactory,
                      )
from sqlalchemy.schema import Column as SAColumn
from testdatautil.schema import Column, Table


class RuleSet(object):
    @classmethod
    def create(cls, default_rule=None, rules=None):
        return cls(default_rule=default_rule, rules=rules)

    @classmethod
    def match(cls, rules, field, table_data, context):
        for priority, rule in rules:
            if rule.match_all(field, table_data, context):
                result = rule.build(field)
                return result

    def __init__(self, default_rule=None, rules=None):
        self._rules = dict()
        self._table_rules = dict()
        self._leng = 0
        self._context = dict()
        if default_rule:
            self.add_rule(default_rule, priority=-123)
        if rules:
            for rule in rules:
                self.add_rule(rule)

    def add_rule(self, rule, priority=None):
        assert isinstance(rule, Rule)
        if priority is None:
            if hasattr(rule, 'base_priority'):
                priority = rule.base_priority
            else:
                priority = self._leng * 10
        # classifying table rules and other rules
        if isinstance(rule, TableRule):
            target = self._table_rules
        else:
            target = self._rules
        while priority in target:
            priority += 1
        target[priority] = rule
        self._leng += 1

    def apply_all(self, metadata, tables):
        context = OrderedDict()
        rules = list(self._rules.items())
        rules.sort(reverse=True)
        table_rules = list(self._table_rules.items())
        table_rules.sort(reverse=True)
        table_factories = OrderedDict()
        for table_data in tables:
            table_name = table_data.name
            context.setdefault(table_name, OrderedDict())
            args = [table_name, metadata]
            for field_name, field in table_data.items():
                factory = self.match(rules, field, table_data,
                                     context)
                args.append(Column(field_name, factory))
                context[table_name][field_name] = factory
            factory = Table(*args)
            table_factories[table_name] = factory

        metadata.tables = table_factories
        return table_factories


class Rule(object):
    def match_all(self, field, table_data, context):
        # base classes rule must much
        for base in self.__class__.mro():
            if issubclass(base, Rule) and base is not Rule:
                if not base.match(self, field=field, table_data=table_data,
                                  context=context):
                    return False
        if self.match(field, table_data, context):
            return True
        return False

    def match(self, field, table_data, context):
        """
        rule match condition

        if match return True, else False.

        :param field: table column
        :param table_data:dict
        :param context:dict
        :return:bool
        """
        raise NotImplemented

    def build(self, field):
        """
        if match, return Factory

        Factory extends testdata.Factory class

        :param field:
        :return:
        """
        raise NotImplemented()


class TableRule(Rule):
    pass


class BottomRule(Rule):
    """
    match always
    """
    def match(self, field, table_data, context):
        return True


class Choice(BottomRule):
    def __init__(self, choices):
        self._choices = choices

    def build(self, field):
        return RandomSelection(sequence=self._choices)


class ConstantNone(BottomRule):
    def build(self, field):
        return Constant(None)


class SqlAlchemyRule(Rule):
    def match(self, field, table_data, context):
        return isinstance(field, SAColumn)

    def build(self, field):
        raise NotImplemented()


class SAFieldNameRule(SqlAlchemyRule):
    fieldname = None

    def match(self, field, table_data, context):
        return self.fieldname == field.name


class SASuffixRule(SqlAlchemyRule):
    suffix = None

    def match(self, field, table_data, context):
        return field.name.endswith(self.suffix)


class SATypeRule(SqlAlchemyRule):
    python_type = None

    def match(self, field, table_data, context):
        return field.type.python_type is self.python_type


class SAInteger(SATypeRule):
    python_type = int

    def build(self, field):
        return RandomInteger(minimum=0, maximum=100)


class SAFloat(SATypeRule):
    python_type = float

    def build(self, field):
        return RandomFloat(minimum=0.0, maximum=100.0)


class SAString(SATypeRule):
    python_type = str

    def build(self, field):
        length = 10
        if hasattr(field, 'length'):
            length = field.length
        if length < 5 or field.unique:
            return RandomLengthStringFactory(min_chars=0, max_chars=length)
        return FakeDataFactory('word')


class SADateTime(SATypeRule):
    python_type = datetime

    def __init__(self, basedate=None):
        if basedate is None:
            basedate = datetime.now() - timedelta(days=2)
        self._basedate = basedate

    def build(self, field):
        base = self._basedate
        return RandomDateFactory(minimum=base, maximum=base + timedelta(days=1))


class SADate(SATypeRule):
    python_type = date

    def __init__(self, basedate=None):
        if basedate is None:
            basedate = date.today() - timedelta(days=10)
        self._basedate = basedate

    def build(self, field):
        base = self._basedate
        return RandomDateFactory(minimum=base, maximum=base + timedelta(days=10))


class SADateTimeSequence(SATypeRule):
    python_type = datetime

    def __init__(self, basedate=None):
        if basedate is None:
            basedate = datetime.now() - timedelta(days=2)
        self._basedate = basedate

    def build(self, field):
        base = self._basedate
        return DateIntervalFactory(base=base, delta=timedelta(seconds=121))


class SADateSequence(SATypeRule):
    python_type = date

    def __init__(self, basedate=None):
        if basedate is None:
            basedate = date.today() - timedelta(days=10)
        self._basedate = basedate

    def build(self, field):
        base = self._basedate
        return DateIntervalFactory(base=base, delta=timedelta(days=1))


class SABoolean(SATypeRule):
    python_type = bool

    def build(self, field):
        return RandomSelection(sequence=(1, 0))


class SAEmail(SASuffixRule):
    suffix = 'mail'

    def build(self, field):
        return FakeDataFactory('email')


class SAName(SASuffixRule):
    suffix = "name"

    def build(self, field):
        return FakeDataFactory('first_name')


class SAAutoIncrement(SAInteger):
    def match(self, field, table_data, context):
        return field.primary_key and field.autoincrement

    def build(self, field):
        return CountingFactory(1)


class SqlAlchemyRuleSet(RuleSet):
    @classmethod
    def create(cls, default_rule=None, rules=None):
        # default sqlalchemy rule set
        basedate = date.today() - timedelta(days=10)
        basedatetime = datetime.now() - timedelta(days=10)
        rule_set = RuleSet.create(default_rule=ConstantNone())
        rule_set.add_rule(SAInteger())
        rule_set.add_rule(SAFloat())
        rule_set.add_rule(SAString())
        rule_set.add_rule(SADateTime(basedatetime))
        rule_set.add_rule(SADate(basedate))
        rule_set.add_rule(SAName())
        rule_set.add_rule(SAEmail())
        rule_set.add_rule(SAAutoIncrement(), priority=9999)
        return rule_set
