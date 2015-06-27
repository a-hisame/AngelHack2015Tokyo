#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Use to DynamoDB Layer
'''

import hashlib
import logging
import boto.dynamodb2

from boto.dynamodb2.table import Table

__GLOBALS = {}

def _put(key, value):
  __GLOBALS[key] = value

def _get(key, else_value=None):
  return __GLOBALS.get(key, else_value)


def connection():
  return _get('conn', None)

def environment():
  return _get('env', None)

def product():
  return _get('product', None)


def initialize(env, product, access_key=None, secret_access_key=None, region='ap-northeast-1'):
  _put('env', env)
  _put('product', product)
  try:
    if access_key is None or secret_access_key is None:
      logging.info(u'Connection created by IAM role')
      conn = boto.dynamodb2.connect_to_region(region)
      _put('conn', conn)
    else:
      logging.info(u'Connection create by Configfile')
      conn = boto.dynamodb2.connect_to_region(region,
          aws_access_key_id=access_key,
          aws_secret_access_key=secret_access_key)
      _put('conn', conn)
  except Exception as e:
    logging.exception(e)
    logging.error('initialized failure')
    raise e


def get_tablename(tablename):
  names = [environment(), product(), tablename]
  return '_'.join(filter(lambda s: s is not None, names))


def get_table(tablename):
  tblname = get_tablename(tablename)
  key = 'table.{0}'.format(tblname)
  cache = _get(key)
  if cache is not None:
    return cache
  table = Table(tblname, connection=connection())
  _put(key, table)
  return table

def item_to_dict(item):
  return { k: item[k] for k in item.keys() }


def get_env(key, else_value=None, update_force=False, tblname='environment'):
  tab = get_table(tblname)
  id = str(hashlib.sha1(key).hexdigest())
  localkey = 'env.{0}'.format(id)
  cache = _get(localkey)
  if cache is not None and update_force is False:
    return cache
  if not tab.has_item(id=id):
    return else_value
  value = tab.get_item(id=id).get('value')
  _put(localkey, value)
  return value

