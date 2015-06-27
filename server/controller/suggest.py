#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
'''

import json
import bottle
from bottle import route, run, view, static_file, template
from bottle import get, post, request, response

__CONTEXT_ROOT = 'hungry'

def _suggest_result(suggest_type, param):
  ''' return suggest json structure '''
  if not param.has_key('prefix'):
    return { 'candidates': [], 'description': 'no item' }
  prefix = param['prefix']
  # search here
  cs = ['Hoge', 'Piyo', 'Fuga', suggest_type]
  description = 'sample'
  return { 'type': suggest_type, 'candidates': cs, 'description': description }


@get('/{0}/api/suggest'.format(__CONTEXT_ROOT))
@get('/{0}/api/suggest/name'.format(__CONTEXT_ROOT))
def suggest_name():
  result = _suggest_result('name', dict(request.query.decode()))
  response.content_type = 'application/json'
  return result 

@get('/{0}/api/suggest/tag'.format(__CONTEXT_ROOT))
def suggest_tag():
  result = _suggest_result('tag', dict(request.query.decode()))
  response.content_type = 'application/json'
  return result 

@get('/{0}/api/suggest/restaurant'.format(__CONTEXT_ROOT))
def suggest_restaurant():
  result = _suggest_result('restaurant', dict(request.query.decode()))
  response.content_type = 'application/json'
  return result 


