#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import csv
import hashlib
import codecs
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
  tab = dao.dynamodb.get_table('tags')
  with codecs.open('in.csv', 'r', 'utf-8') as fh:
    itr = csv.reader(fh)
    for row in itr:
      tab.put_item(data={
        'id': str(hashlib.sha1(row[0]).hexdigest()),
        'name_en': row[0],
      }, overwrite=True)

