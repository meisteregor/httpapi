# -*- coding: utf-8 -*-

port = 5000
path = 'test_data'
db = 'index.db'


def init_config(args):
    globals()['port'] = args.port
    globals()['path'] = args.data
    globals()['db'] = args.db
