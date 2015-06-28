#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Use to Amazon S3 Layer
'''

import hashlib
import logging

import boto.s3
from boto.s3.key import Key


__GLOBALS = {}

def _put(key, value):
  __GLOBALS[key] = value

def _get(key, else_value=None):
  return __GLOBALS.get(key, else_value)


def connection():
  return _get('conn', None)

def initialize(access_key=None, secret_access_key=None, region='ap-northeast-1'):
  try:
    if access_key is None or secret_access_key is None:
      logging.info(u'Connection created by IAM role')
      conn = boto.s3.connect_to_region(region)
      _put('conn', conn)
    else:
      logging.info(u'Connection create by Configfile')
      conn = boto.s3.connect_to_region(region,
          aws_access_key_id=access_key,
          aws_secret_access_key=secret_access_key)
      _put('conn', conn)
  except Exception as e:
    logging.exception(e)
    logging.error('initialized failure')
    raise e


def upload(localfile, s3bucket, uploadpath):
  conn = connection()
  bucket = conn.get_bucket(s3bucket)
  key = Key(bucket, uploadpath)
  key.set_contents_from_filename(localfile)


