#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import bottle
from bottle import route, run, view, static_file
from bottle import get, post, request

def get_current_dir():
  return os.path.dirname(os.path.abspath(__file__))

# append path relative to this file
bottle.TEMPLATE_PATH.append(os.path.join(get_current_dir(), '..', 'views/'))

@route('/css/<filename>')
def css_static(filename):
  ''' append routing for css files '''
  css_root = os.path.join(get_current_dir(), '..', 'css')
  return static_file(filename, root=css_root)

@route('/js/<filename>')
def js_static(filename):
  ''' append routing for js files '''
  js_root = os.path.join(get_current_dir(), '..', 'js')
  return static_file(filename, root=js_root)

@route('/images/<filename>')
def imgs_static(filename):
  ''' append routing for image files '''
  img_root = os.path.join(get_current_dir(), '..', 'images')
  return static_file(filename, root=img_root)

@route('/fonts/<filename>')
def font_static(filename):
  ''' append routing for fonts files '''
  font_root = os.path.join(get_current_dir(), '..', 'fonts')
  return static_file(filename, root=font_root)

