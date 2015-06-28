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
  tab = dynamodb.get_table('dishes')
  id = params.get('id')
  if not tab.has_item(id=id):
    return None
  return dynamodb.item_to_dict(tab.get_item(id=id))


@get('/{0}/api/dish'.format(__CONTEXT_ROOT))
def get_search_dish():
  result = _get_dish(dict(request.query.decode()))
  response.content_type = 'application/json'
  return {
    'found': result is not None,
    'result': result,
  }


def _get_dish_images(params, else_value=None):
  tab = dynamodb.get_table('dishes')
  name = params.get('name')
  if name is None:
    return []

  imgs = []
  for item in tab.scan():
    d = dynamodb.item_to_dict(item)
    if d.get('name_en', '') != name:
      continue
    path = d.get('path')
    if path is None:
      continue
    imgs.append(path)
    if len(imgs) >= 5:
      break

  return imgs


@get('/{0}/api/dish/images'.format(__CONTEXT_ROOT))
def get_dish_images():
  result = _get_dish_images(dict(request.query.decode()))
  response.content_type = 'application/json'
  return {
    'found': result is not None,
    'urls': result,
  }


