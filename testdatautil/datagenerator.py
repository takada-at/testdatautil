# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from datetime import datetime, date
import csv
import json
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
    ext = '.txt'

    def __init__(self, directory, length):
        self._directory = directory
        self._length = length

    def write(self, table_name, dataschema):
        filename = "{}{}".format(table_name, self.ext)
        path = os.path.join(self._directory, filename)
        with open(path, 'w') as fio:
            self.write_file(dataschema, file_handle=fio)

    def write_file(self, dataschema, file_handle):
        raise NotImplemented()


class PythonFormatter(Formatter):
    ext = '.py'

    def __init__(self, directory, length):
        self._directory = directory
        self._length = length
        filename = 'mockdata.py'
        path = os.path.join(self._directory, filename)
        self._file_handle = open(path,'w')

    def write(self, table_name, dataschema):
        self.write_file(dataschema, file_handle=self._file_handle)

    def write_file(self, dataschema, file_handle):
        file_handle.write('{} = [\n'.format(dataschema.name))
        for data in dataschema.generate(self._length):
            file_handle.write('    {},\n'.format(repr(dict(data))))

        file_handle.write(']\n')


class JsonFormatter(Formatter):
    ext = '.json'

    def write_file(self, dataschema, file_handle):
        for data in dataschema.generate(self._length):
            formatted = formatdict(data)
            jsondata = json.dumps(formatted)
            file_handle.write(jsondata + "\n")


class CsvFormatter(Formatter):
    def __init__(self, directory, length, sep=b",",
                 write_header=True):
        self._directory = directory
        self._length = length
        self._sep = sep
        self._write_header = write_header

    def write_file(self, dataschema, file_handle):
        writer = csv.writer(file_handle,
                            delimiter=self._sep.decode("utf-8"))
        keys = dataschema.keys()
        if self._write_header:
            writer.writerow([key for key in keys])
        for data in dataschema.generate(self._length):
            formatted = formatdict(data)
            writer.writerow([formatted[key] for key in keys])


class DataGenerator(object):
    def __init__(self, metadata, directory,
                 table_names, sep=b',',
                 write_header=True,
                 format='csv',
                 length=10, formatter=None):
        if not table_names:
            table_names = list(metadata.tables.keys())
        self._metadata = metadata
        self._table_names = table_names
        self._length = length
        if formatter is None:
            if format == 'python':
                formatter = PythonFormatter(directory, length)
            elif format == 'json':
                formatter = JsonFormatter(directory, length)
            else:
                formatter = CsvFormatter(directory, length, sep=sep,
                                         write_header=write_header)

        self._formatter = formatter

    def generate(self):
        items = self._metadata.tables
        for table_name in self._table_names:
            if table_name in items:
                schema = items[table_name]
                self._formatter.write(table_name, schema)
