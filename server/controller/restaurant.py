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


def _restaurant_namelist(params):
  dishes = dynamodb.get_table('dishes')
  restaurant_name = params.get('restaurant')
  if restaurant_name is None:
    return []

  ds = dishes.scan(restaurant__beginswith=restaurant_name)
  nameset = set()
  for item in ds:
    name = item.get('restaurant')
    if name is None or not name.startswith(restaurant_name):
      continue
    nameset.add(name)
  return list(nameset)


def _item_to_restaurant_result(item):
  d = dynamodb.item_to_dict(item)
  imagepath = '{0}{1}/{2}'.format(
      dynamodb.get_env('IMAGE_SERVER_PREFIX'),
      dynamodb.get_env('IMAGE_SERVER'),
      item.get('path'))
  return {
    'name': d.get('name_en', ''),
    'path': imagepath if d.has_key('path') else '', 
  }


def _search_restaurantlist(names, page=None, limit=9):
  page = 1 if page is None else page
  starts = (page - 1) * limit
  ends = page * limit
  keys = map(lambda s: str(hashlib.sha1(s).hexdigest()), names[starts:ends])

  results = []
  tab = dynamodb.get_table('restaurant')
  for key in keys:
    if tab.has_item(id=key):
      results.append(tab.get_item(id=key))

  return {
    'page': page,
    'limit': limit,
    'restaurants': [ _item_to_restaurant_result(item) for item in results ],
  }

@get('/{0}/api/search/restaurant'.format(__CONTEXT_ROOT))
def get_search_restaurant_list():
  names = _restaurant_namelist(dict(request.query.decode()))
  results = _search_restaurantlist(names)  
  response.content_type = 'application/json'
  return results


