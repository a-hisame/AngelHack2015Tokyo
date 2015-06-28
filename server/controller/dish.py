#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
'''

import json
import bottle
from bottle import route, run, view, static_file, template
from bottle import get, post, request, response
import hashlib

import dao.dynamodb as dynamodb

__CONTEXT_ROOT = 'hungry'

def _get_dish(params, else_value=None):
  tab = dynamodb.get_table('dish')
  name = params.get('name')
#  id = str(hashlib.sha1(name).hexdigest())
#  if not tab.has_item('name_en'=name):
#    return else_value
#  item = tab.get_item('name_en'=name)
  items = tab.scan(name_en__beginswith=name) 
  scanned = [ dynamodb.item_to_dict(item) for item in items ]

  candidates = sorted(scanned, cmp=lambda a,b: cmp(a['name_en'], b['name_en']))[0:5]
  cand_list = []
  cand_list = [ c['id'] for c in candidates ]


  return {
#    'name': item['name_en'],
    'name': 'hoge',
  }


@get('/{0}/api/dish'.format(__CONTEXT_ROOT))
def get_search_dish():
  result = _get_dish(dict(request.query.decode()))
  response.content_type = 'application/json'
  return result 


