# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from datetime import datetime, date
import csv
import os


def formatdict(dictdata):
    result = dict()
    for key, val in dictdata.items():
        if isinstance(val, datetime):
            nval = datetime.strftime(val, "%Y-%m-%d %H:%M:%S")
        elif isinstance(val, date):
            nval = date.strftime(val, "%Y-%m-%d")
        elif val is None:
            nval = ''
        elif isinstance(val, bool):
            nval = "1" if val else "0"
        else:
            nval = str(val)
        result[key] = nval
    return result


class Formatter(object):
    pass


class CsvFormatter(Formatter):
    def __init__(self, directory, length, sep=b",",
                 write_header=True):
        self._directory = directory
        self._length = length
        self._sep = sep
        self._write_header = write_header

    def write(self, table_name, dataschema):
        filename = "{}.csv".format(table_name)
        path = os.path.join(self._directory, filename)
        assert os.path.exists(self._directory)
        with open(path, 'w') as fio:
            keys = dataschema.keys()
            writer = csv.DictWriter(fio, fieldnames=keys)
            if self._write_header:
                writer.writeheader()
            for data in dataschema.generate(self._length):
                writer.writerow(formatdict(data))


class DataGenerator(object):
    def __init__(self, metadata, directory,
                 table_names, sep=b',',
                 write_header=True,
                 length=10, formatter=None):
        if not table_names:
            table_names = list(metadata.tables.keys())
        self._metadata = metadata
        self._table_names = table_names
        self._length = length
        if formatter is None:
            formatter = CsvFormatter(directory, length, sep=sep,
                                     write_header=write_header)
        self._formatter = formatter

    def generate(self):
        items = self._metadata.tables
        for table_name in self._table_names:
            if table_name in items:
                schema = items[table_name]
                self._formatter.write(table_name, schema)
