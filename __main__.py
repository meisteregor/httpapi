# -*- coding: utf-8 -*-

import argparse
import pysearch

parser = argparse.ArgumentParser()
parser.add_argument('mode', help='Run mode, one of `index` or `service`')
parser.add_argument('--port', help='Service listen port, default 5000', type=int, default=5000)
parser.add_argument('--db', help='Path to index db file, default index.db', default='index.db')
parser.add_argument('--data', help='Path to the input data dir, default test_data/', default='test_data')

args = parser.parse_args()
pysearch.settings.init_config(args)

if args.mode == 'index':
    pysearch.indexer.main()
else:
    pysearch.service.run_server()
