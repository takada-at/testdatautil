# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from faker import Faker
from factory.declarations import OrderedDeclaration
from factory.fuzzy import BaseFuzzyAttribute


class DateIntervalFactory(OrderedDeclaration):
    def __init__(self, base, delta):
        self.base = base
        self.delta = delta

    def evaluate(self, sequence, obj, create, extra=None, containers=()):
        return self.base + self.delta * sequence


class FakeDataFactory(BaseFuzzyAttribute):
    def __init__(self, factory_name):
        self.fake = Faker()
        self.factory_name = factory_name

    def fuzz(self):
        return getattr(self.fake, self.factory_name)()


class WordFactory(BaseFuzzyAttribute):
    def __init__(self, length=20):
        self.fake = Faker()
        self.length = length
        super(WordFactory, self).__init__()

    def fuzz(self):
        word = self.fake.word()
        return word[:self.length]
