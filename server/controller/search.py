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
    'priority': item.get('_cmp', 999999999),
    'name': item.get('name_en'),
    'description': item.get('description', ''),
    'tags': item.get('tags', '').split(','),
    'image': imagepath if item.has_key('path') else '', 
  }

def _search_dish(params):
  tab = dynamodb.get_table('dishes')
  keywords = params.get('keyword', '')
  itemfrom = int(params.get('itemfrom', '0'))
  itemto = int(params.get('itemto', '10'))

  ks = keywords.split(',')

  allitems = [ dynamodb.item_to_dict(item) for item in tab.scan() ]


  def _to_cmp(d, else_value=None):
    # match names
    name = d.get('name_en', '') 
    if name in ks:
      return 0
    # complete equal: tags
    ts = d.get('tags', '').split(',')
    count = 0
    for keyword in ks:
      if keyword in ts:
        count = count + 1
    if count > 0:
      return 1 + 50 - int(float(count) / float(len(ts)) * 50)

   # imcomplete equals 
    count = 0
    for keyword in ks:
      if name.find(keyword) >= 0:
        return 100
      for tag in ts:
        if tag.find(keyword) >= 0:
          count = count + 1
    if count > 0:
      return 100 + len(ts) - count
    # not matched
    return else_value
  
  results = []
  for dish in allitems:
    cmpvalue = _to_cmp(dish)
    if cmpvalue is None:
      continue
    dish['_cmp'] = cmpvalue
    results.append(dish)
  
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

