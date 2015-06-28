#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import argparse

from bottle import run

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import dao.dynamodb
import dao.s3

import controller.static
import controller.index
import controller.suggest
import controller.search
import controller.upload


def _parser():
  parser = argparse.ArgumentParser()
  parser.add_argument('--accesskey', type=str, required=False, default=None)
  parser.add_argument('--secretkey', type=str, required=False, default=None)
  return parser

if __name__ == '__main__':
  args = _parser().parse_args(sys.argv[1:])
  dao.dynamodb.initialize('production', 'bhukha', args.accesskey, args.secretkey)
  dao.s3.initialize(args.accesskey, args.secretkey)
  run(host='0.0.0.0', port=8080)

