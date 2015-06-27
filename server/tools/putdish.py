#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import csv
import hashlib
import codecs
import datetime
import argparse

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import dao.dynamodb

def _parser():
  parser = argparse.ArgumentParser()
  parser.add_argument('--accesskey', type=str, required=False, default=None)
  parser.add_argument('--secretkey', type=str, required=False, default=None)
  return parser

if __name__ == '__main__':
  args = _parser().parse_args(sys.argv[1:])
  dao.dynamodb.initialize('production', 'bhukha', args.accesskey, args.secretkey)
  tab = dao.dynamodb.get_table('dishes')
  with codecs.open('dummy.csv', 'r', 'utf-8') as fh:
    itr = csv.reader(fh)
    with tab.batch_write() as batch:
      for row in itr:
        print row[0]
        dt = datetime.datetime.now()
        registed = dt.strftime('%Y%m%d%H%M%S.%f')
        id = str(hashlib.sha1('^{0}#{1}$'.format(row[0], registed)).hexdigest())
        tab.put_item(data={
          'id': id,
          'name_en': row[0],
          'description': row[1],
          'restaurant': row[2],
          'tags': row[3],
          'registed': registed,
        }, overwrite=True)

