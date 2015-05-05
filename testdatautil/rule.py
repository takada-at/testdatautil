# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from collections import OrderedDict
from datetime import datetime, date, timedelta
from testdata import (RandomInteger, Constant, RandomSelection,
                      RandomLengthStringFactory,
                      RandomDateFactory, RandomFloat,
                      FakeDataFactory, CountingFactory,
                      )
from sqlalchemy.schema import Column


class RuleSet(object):
    @classmethod
    def create(cls, default_rule=None, rules=None):
        return cls(default_rule=default_rule, rules=rules)

    def __init__(self, default_rule=None, rules=None):
        self._rules = dict()
        self._leng = 0
        self._context = dict()
        if default_rule:
            self.add(default_rule, priority=-123)
        if rules:
            for rule in rules:
                self.add(rule)

    def add(self, rule, priority=None):
        assert isinstance(rule, Rule)
        if priority is None:
            priority = self._leng * 10
        while priority in self._rules:
            priority += 1
        self._rules[priority] = rule
        self._leng += 1

    def apply_all(self, tables):
        context = OrderedDict()
        rules = list(self._rules.items())
        rules.sort(reverse=True)
        for table_name, table_data in tables.items():
            context.setdefault(table_name, OrderedDict())
            for field_name, field in table_data.items():
                result = self.match(rules, field, table_data,
                                    context)
                context[table_name][field_name] = result
        return context

    @classmethod
    def match(cls, rules, field, table_data, context):
        for priority, rule in rules:
            if rule.match_all(field, table_data, context):
                result = rule.apply(field)
                return result


class Rule(object):
    def match_all(self, field, table_data, context):
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

        :param field:
        :param table_data:
        :param context:
        :return:
        """
        raise NotImplemented

    def apply(self, field):
        """
        if match, return DataFactory

        DataFactory extends testdata.Factory class

        :param field:
        :return:
        """
        raise NotImplemented()


class BottomRule(Rule):
    """
    match always
    """
    def match(self, field, table_data, context):
        return True


class Choice(BottomRule):
    def __init__(self, choices):
        self._choices = choices

    def apply(self, field):
        return RandomSelection(sequence=self._choices)


class ConstantNone(BottomRule):
    def apply(self, field):
        return Constant(None)


class SqlAlchemyRule(Rule):
    def match(self, field, table_data, context):
        return isinstance(field, Column)

    def apply(self, field):
        raise NotImplemented()


class SAFieldNameRule(SqlAlchemyRule):
    __fieldname__ = None

    def match(self, field, table_data, context):
        return self.__fieldname__ == field.name


class SASuffixRule(SqlAlchemyRule):
    suffix = None

    def match(self, field, table_data, context):
        return field.name.endswith(self.suffix)


class SATypeRule(SqlAlchemyRule):
    __python_type__ = None

    def match(self, field, table_data, context):
        return field.type.python_type is self.__python_type__


class SAInteger(SATypeRule):
    __python_type__ = int

    def apply(self, field):
        return RandomInteger(minimum=0, maximum=100)


class SAFloat(SATypeRule):
    __python_type__ = float

    def apply(self, field):
        return RandomFloat(minimum=0.0, maximum=100.0)


class SAString(SATypeRule):
    __python_type__ = str

    def apply(self, field):
        length = 10
        if hasattr(field, 'length'):
            length = field.length
        if length < 5 or field.unique:
            return RandomLengthStringFactory(min_chars=0, max_chars=length)
        return FakeDataFactory('word')


class SADateTime(SATypeRule):
    __python_type__ = datetime

    def __init__(self, basedate=None):
        if basedate is None:
            basedate = datetime.now() - timedelta(days=2)
        self._basedate = basedate

    def apply(self, field):
        base = self._basedate
        return RandomDateFactory(minimum=base, maximum=base + timedelta(days=1))


class SADate(SATypeRule):
    __python_type__ = date

    def __init__(self, basedate=None):
        if basedate is None:
            basedate = date.today() - timedelta(days=10)
        self._basedate = basedate

    def apply(self, field):
        base = self._basedate
        return RandomDateFactory(minimum=base, maximum=base + timedelta(days=10))


class SABoolean(SATypeRule):
    __python_type__ = bool

    def apply(self, field):
        return RandomSelection(sequence=(1, 0))


class SAEmail(SASuffixRule):
    suffix = 'mail'

    def apply(self, field):
        return FakeDataFactory('email')


class SAName(SASuffixRule):
    suffix = "name"

    def apply(self, field):
        return FakeDataFactory('first_name')


class SAAutoIncrement(SAInteger):
    def match(self, field, table_data, context):
        return field.primary_key and field.autoincrement

    def apply(self, field):
        return CountingFactory(1)


class SqlAlchemyRuleSet(RuleSet):
    @classmethod
    def create(cls, default_rule=None, rules=None):
        basedate = date.today() - timedelta(days=10)
        basedatetime = datetime.now() - timedelta(days=10)
        rule_set = RuleSet.create(default_rule=ConstantNone())
        rule_set.add(SAInteger())
        rule_set.add(SAFloat())
        rule_set.add(SAString())
        rule_set.add(SADateTime(basedatetime))
        rule_set.add(SADate(basedate))
        rule_set.add(SAName())
        rule_set.add(SAEmail())
        rule_set.add(SAAutoIncrement(), priority=9999)
        return rule_set
