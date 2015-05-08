# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from setuptools import setup, find_packages


setup(
    name="testdatautil",
    version='0.0.1',
    author="takada-at",
    author_email="takada-at@klab.com",
    description="testdata-utility",
    url="http://github.com/takada-at/testdatautil",
    license="MIT",
    install_requires=[
        'fake-factory >= 0.5'
    ],
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: MIT License",
    ],
)

