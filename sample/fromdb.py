# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import os
import sys
sys.path.append(
    os.path.join(os.path.dirname(__file__),
                 '..')
)
from testdatautil import cli, dataset
from testdatautil.rule import SqlAlchemyRuleSet
from sqlalchemy import create_engine
from sqlalchemy import MetaData


def connect(args):
    url = 'mysql+pymysql://{user}:{password}@{host}/{db}'.format(user=args.user,
                                                                 password=args.password,
                                                                 host=args.host,
                                                                 db=args.db)
    engine = create_engine(url)
    return engine


def main():
    command = cli.Command()
    parser = command.get_parser()
    parser.add_argument('-d', '--db')
    parser.add_argument('--host', default='localhost')
    parser.add_argument('-u', '--user')
    parser.add_argument('-p', '--password')
    args = parser.parse_args()
    rule = SqlAlchemyRuleSet.create()
    engine = connect(args)
    meta = MetaData()
    meta.reflect(bind=engine)
    testdatameta = dataset.from_sqlalchemy_tables(meta.sorted_tables,
                                                  rule_set=rule)
    command.execute(args, testdatameta)


if __name__ == '__main__':
    main()