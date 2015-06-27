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
  tag_tab = dao.dynamodb.get_table('tags')
  new_tags = set()
  for item in [ dao.dynamodb.item_to_dict(i) for i in tab.scan() ]:
    tags = item.get('tags', '')
    if tags == '':
      continue
    for tag in tags.split(','):
      id = str(hashlib.sha1(tag).hexdigest())
      if tag_tab.has_item(id=id):
        continue
      new_tags.add(tag)
  print new_tags
  with tag_tab.batch_write() as batch:
    for tag in new_tags:
      id = str(hashlib.sha1(tag).hexdigest())
      batch.put_item(data={
        'id': id,
        'name_en': tag,
      }, overwrite=True)

