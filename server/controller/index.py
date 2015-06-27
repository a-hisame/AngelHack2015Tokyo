#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
'''

import json
import bottle
from bottle import route, run, view, static_file, template
from bottle import get, post, request, response

__CONTEXT_ROOT = 'hungry'

def _suggest_result(p):
  ''' return suggest json structure '''
  if not p.has_key('prefix'):
    return { 'candidates': [], 'description': 'no item' }
  prefix = p['prefix']
  # search here
  cs = ['Hoge', 'Piyo', 'Fuga']
  description = 'sample'
  return { 'candidates': cs, 'description': description }


@get('/{0}/api/suggest'.format(__CONTEXT_ROOT))
def suggest():
  result = _suggest_result(dict(request.query.decode()))
  response.content_type = 'application/json'
  return result 


@get('/{0}'.format(__CONTEXT_ROOT))
@get('/{0}/index'.format(__CONTEXT_ROOT))
@view('index')
def index():
  ''' return index view '''
  return {}


