# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import argparse
import os
import sys
from .datagenerator import DataGenerator


class Command(object):
    def __init__(self, argv=None):
        self.argv = argv or sys.argv[1:]
        self.prog_name = os.path.basename(sys.argv[0])

    def get_parser(self):
        parser = argparse.ArgumentParser(prog=self.prog_name)
        parser.add_argument('-o', metavar="output", dest="directory",
                            type=os.path.expanduser,
                            default=os.path.expanduser('./data'),
                            help="save directory")
        parser.add_argument('-f', '--format', default='csv', choices=('csv', 'python', 'json'))
        parser.add_argument('-s', '--sep', default=b',',
                            help='csv option. delimiter')
        parser.add_argument('-r', '--repeat',
                            default=10, type=int)
        parser.add_argument('--no-header',
                            dest='noheader',
                            action='store_true',
                            help='csv option. write column name')
        parser.add_argument('--tables', action='store', nargs='*')
        return parser

    def execute(self, args, metadata):
        if not os.path.exists(args.directory):
            print('create directory {}'.format(args.directory))
            os.mkdir(args.directory)

        generator = DataGenerator(metadata=metadata, directory=args.directory,
                                  table_names=args.tables, sep=args.sep,
                                  length=args.repeat,
                                  format=args.format,
                                  write_header=not args.noheader,
                                  )
        generator.generate()


def execute_from_command_line(argv=None, metadata=None):
    command = Command(argv)
    parser = command.get_parser()
    args = parser.parse_args(command.argv)
    command.execute(args, metadata)
