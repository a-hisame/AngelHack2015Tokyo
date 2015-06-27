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
  tab = dynamodb.get_table(suggest_type)
  items = tab.scan(name_en__beginswith=prefix) 
  scanned = [ dynamodb.item_to_dict(item) for item in items ]

  candidates = sorted(scanned, cmp=lambda a,b: cmp(a['name_en'], b['name_en']))[0:5]
  cand_list = []
  cand_list = [ c['name_en'] for c in candidates ]

  return cand_list

def _form_suggestions(suggestions):
  return {
    'type': 'name', 'candidates': suggestions ,
    'matched': len(suggestions),
    'description': 'found {0} items'.format(len(suggestions)),
  }

@get('/{0}/api/suggest'.format(__CONTEXT_ROOT))


@get('/{0}/api/suggest/search'.format(__CONTEXT_ROOT))
def suggest_search():
  suggestions = _suggest_result('dishes', dict(request.query.decode()))
  suggestions.extend(_suggest_result('tags', dict(request.query.decode())))
  response.content_type = 'application/json'
  return _form_suggestions(suggestions)

@get('/{0}/api/suggest/name'.format(__CONTEXT_ROOT))
def suggest_name():
  suggestions = _suggest_result('dishes', dict(request.query.decode()))
  response.content_type = 'application/json'
  return _form_suggestions(suggestions)

@get('/{0}/api/suggest/tag'.format(__CONTEXT_ROOT))
def suggest_tag():
  suggestions = _suggest_result('tags', dict(request.query.decode()))
  response.content_type = 'application/json'
  return _form_suggestions(suggestions)


@get('/{0}/api/suggest/restaurant'.format(__CONTEXT_ROOT))
def suggest_restaurant():
  suggestions = _suggest_result('restaurant', dict(request.query.decode()))
  response.content_type = 'application/json'
  return _form_suggestions(suggestions)


