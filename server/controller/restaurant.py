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

def _get_restaurant(params, else_value=None):
  tab = dynamodb.get_table('restaurant')
  name = params.get('name', '')
  id = str(hashlib.sha1(name).hexdigest())
  if not tab.has_item(id=id):
    return else_value
  item = tab.get_item(id=id)

  return {
    'name': item['name_en'],
    'path': item['path'],
  }


@get('/{0}/api/search/restaurant'.format(__CONTEXT_ROOT))
def get_search_restaurant():
  result = _get_restaurant(dict(request.query.decode()))
  response.content_type = 'application/json'
  return result 

@post('/{0}/api/search/restaurant'.format(__CONTEXT_ROOT))
def get_search_restaurant():
  result = _get_restaurant(dict(request.forms.decode()))
  response.content_type = 'application/json'
  return result 

