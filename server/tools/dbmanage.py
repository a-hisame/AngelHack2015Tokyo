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

  with tab.batch_write() as batch:
    for item in tab.scan():
      if 'description' not in item.keys():
        batch.delete_item(id=item['id'])

