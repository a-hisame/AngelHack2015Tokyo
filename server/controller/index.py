#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
'''

import bottle
from bottle import route, run, view, static_file, template
from bottle import get, post, request

__CONTEXT_ROOT = 'hungry'

@get('/{0}'.format(__CONTEXT_ROOT))
@get('/{0}/index'.format(__CONTEXT_ROOT))
@view('views/index')
def index():
  ''' return index view '''
  return {}

