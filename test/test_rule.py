# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from testdatautil.rule import Rule, RuleSet


class RuleBy2(Rule):
    def match(self, field, context):
        return field % 2 == 0

    def build(self, field):
        return "2"


class RuleBy3(Rule):
    def match(self, field, context):
        return field % 3 == 0

    def build(self, field):
        return "3"


def test_ruleset():
    rule_set = RuleSet()
    rule_set.add_rule(RuleBy2())
    rule_set.add_rule(RuleBy3())

    # rule by 3 apply
    res = rule_set.match(rule_set.rules, 6, None)
    assert "3" == res

    res = rule_set.match(rule_set.rules, 4, None)
    assert "2" == res

    res = rule_set.match(rule_set.rules, 5, None)
    assert res is None

    res = rule_set.match(rule_set.rules, 3, None)
    assert "3" == res
