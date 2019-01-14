# -*- coding: utf-8 -*-

import glob
import json
import os
import sqlite3
import time
from pysearch import settings


def _index_obj(file_id, data, obj, lvl=0):
    if lvl >= 3:
        return
    if isinstance(obj, dict):
        keys = [s.lower() for s in obj.keys() if isinstance(s, str)]
        values = obj.values()
        for k in keys:
            if k not in data['keys']:
                data['keys'][k] = set()
            data['keys'][k].add(file_id)
        for v in values:
            _index_obj(file_id, data, v, lvl + 1)
    elif isinstance(obj, list):
        for v in obj:
            _index_obj(file_id, data, v, lvl + 1)
    else:
        value = str(obj).lower()
        if value not in data['values']:
            data['values'][value] = set()
        data['values'][value].add(file_id)


def _index_files(dir_, files=None, all_data=None):
    if all_data is None:
        all_data = {'keys': {}, 'values': {}, 'files': {}}
    if files is None:
        files = {}
    if os.path.isdir(dir_):
        for d in glob.glob(dir_ + '/*'):
            _index_files(d, files, all_data)
    elif os.path.isfile(dir_) and dir_.endswith('.json'):
        data = None
        try:
            with open(dir_) as f:
                data = json.loads(f.read())
        except RuntimeError as e:
            print("Error reading file " + dir_ + ": " + str(e))
            pass
        if data:
            print(dir_)
            if dir_ not in files:
                files[dir_] = len(files)
            file_id = files[dir_]
            _index_obj(file_id, all_data, data)

    all_data['files'] = files
    return all_data


def _run_indexer(db_f, data_dir):
    if not os.path.exists(data_dir) or not os.listdir(data_dir):
        raise ValueError("Enter a valid path to data")
    if os.path.exists(db_f):
        os.unlink(db_f)

    db = sqlite3.connect(db_f)
    db.execute("""
        create table values_idx (value varchar(255) not null, files text not null, primary key (value))
    """)
    db.execute("""
        create table keys_idx (value varchar(255) not null, files text not null, primary key (value))
    """)
    db.execute("""
        create table files (id integer primary key, path varchar(255) not null)
    """)

    print('!!! Building indices')
    res = _index_files(os.path.abspath(data_dir))
    res['files'] = [[res['files'][k], k] for k in res['files']]
    res['keys'] = [[k, ','.join(map(str, res['keys'][k]))] for k in res['keys']]
    res['values'] = [[k, ','.join(map(str, res['values'][k]))] for k in res['values']]

    print('!!! Inserting values ...')
    db.executemany('insert into values_idx (value, files) values (?, ?)', res['values'])
    print('!!! Inserting keys ...')
    db.executemany('insert into keys_idx (value, files) values (?, ?)', res['keys'])
    print('!!! Inserting files ...')
    db.executemany('insert into files (id, path) values (?, ?)', res['files'])

    db.commit()
    print('!!! All done')


def main():
    start_time = time.time()
    _run_indexer(settings.db, settings.path)
    print("--- %s seconds ---" % (time.time() - start_time))
