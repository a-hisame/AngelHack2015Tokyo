#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
'''

import json
import bottle
from bottle import route, run, view, static_file, template
from bottle import get, post, request, response

import dao.dynamodb as dynamodb

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

def _suggest_tag(param):
  if not param.has_key('prefix'):
    return { 'type': 'tag', 'candidates': [], 'description': 'no item' }
  prefix = param['prefix']
  tab = dynamodb.get_table('tags')
  items = tab.scan(name_en__beginswith=prefix) 
  scanned = [ dynamodb.item_to_dict(item) for item in items ]
  candidates = sorted(scanned, cmp=lambda a,b: cmp(a['name_en'], b['name_en']))[0:5]
  return {
    'type': 'tag', 'candidates': [ c['name_en'] for c in candidates ],
    'matched': len(scanned),
    'description': 'found {0} items'.format(len(scanned)),
  }

@get('/{0}/api/suggest/tag'.format(__CONTEXT_ROOT))
def suggest_tag():
  result = _suggest_tag(dict(request.query.decode()))
  response.content_type = 'application/json'
  return result 

@get('/{0}/api/suggest/restaurant'.format(__CONTEXT_ROOT))
def suggest_restaurant():
  result = _suggest_result('restaurant', dict(request.query.decode()))
  response.content_type = 'application/json'
  return result 

