# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from faker import Faker
from testdata import Factory, CountingFactory


class DependentFactory(Factory):
    def __init__(self, base_factory):
        self._base_factories = [base_factory]

    def __iter__(self):
        super(DependentFactory, self).__iter__()
        base_factories = []
        for base in self._base_factories:
            base_factories.append(iter(base))

        self._base_factories = base_factories

    def set_element_amount(self, new_element_amount):
        super(DependentFactory, self).set_element_amount(new_element_amount)
        for base in self._base_factories:
            base.set_element_amount = new_element_amount

    def __call__(self):
        raise NotImplementedError()

    def increase_index(self):
        super(DependentFactory, self).increase_index()
        for base in self._base_factories:
            base.increse_index()


class WordFactory(Factory):
    def __init__(self, length=20):
        self.fake = Faker()
        self.length = length
        super(WordFactory, self).__init__()

    def __call__(self):
        word = self.fake.word()
        return word[:self.length]


class PrefixedCountingFactory(CountingFactory):
    def __init__(self, prefix, start_value=0, step=1):
        super(PrefixedCountingFactory, self).__init__(start_value=start_value,
                                                      step=step)
        self.prefix = prefix

    def __call__(self):
        retval = super(PrefixedCountingFactory, self).__call__()
        return "{}{}".format(self.prefix, retval)
