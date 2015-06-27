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

def _dish_to_json_dict(order, item):
  imagepath = '{0}{1}/{2}'.format(
      dynamodb.get_env('IMAGE_SERVER_PREFIX'),
      dynamodb.get_env('IMAGE_SERVER'),
      item.get('path'))
  return {
    'order': order,
    'name': item.get('name_en'),
    'description': item.get('description', ''),
    'tags': item.get('tags', '').split(','),
    'image': imagepath if item.has_key('path') else '', 
  }

def _search_dish(params):
  tab = dynamodb.get_table('dishes')
  keyword = params.get('keyword', '')
  itemfrom = int(params.get('itemfrom', '0'))
  itemto = int(params.get('itemto', '10'))

  names = [ dynamodb.item_to_dict(item) for item in tab.scan(name_en__contains=keyword) ]
  tags = [ dynamodb.item_to_dict(item) for item in tab.scan(tags__contains=keyword) ]

  def _to_cmp(d):
    name = d.get('name_en', '') 
    if name == keyword:
      return 0
    ts = d.get('tags', '').split(',')
    if keyword in ts:
      return 1
    if name.find(keyword) >= 0:
      return 2
    return 3
  
  results = []
  ids = set()
  for dish in (names + tags):
    id = dish.get('id', None)
    if id is None or id in ids:
      continue
    dish['_cmp'] = _to_cmp(dish)
    results.append(dish)
    ids.add(id)
  
  cmpfunc = lambda a,b: cmp( (a['_cmp'], a.get('name_en')), (b['_cmp'], b.get('name_en')))
  ordered = sorted(results, cmp=cmpfunc)
  
  return {
    'result': [_dish_to_json_dict(itemfrom + idx, item) for (idx, item) in enumerate(ordered[itemfrom:itemto]) ],
    'count': len(ordered[itemfrom:itemto]),
    'beginindex': itemfrom,
    'total': len(ordered),
  }


@post('/{0}/api/search/dishes'.format(__CONTEXT_ROOT))
def post_search_dish():
  result = _search_dish(dict(request.forms.decode()))
  response.content_type = 'application/json'
  return result 


@get('/{0}/api/search/dishes'.format(__CONTEXT_ROOT))
def get_search_dish():
  result = _search_dish(dict(request.query.decode()))
  response.content_type = 'application/json'
  return result 

