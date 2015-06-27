#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
'''

import os
import uuid
import json

import bottle
from bottle import route, run, view, static_file, template
from bottle import get, post, request, response
from bottle import HTTPError

__CONTEXT_ROOT = 'hungry'

@get('/{0}/upload'.format(__CONTEXT_ROOT))
@view('upload')
def upload():
  return {}

def _validate_uploaded(filename):
  f = filename.lower()
  suffixes = ['.png', '.jpg', '.jpeg']
  for suffix in suffixes:
    if f.endswith(suffix):
      return True
  return False


@post('/{0}/api/upload'.format(__CONTEXT_ROOT))
def upload_image():
  uploaded = request.files.get('upload')
  if not _validate_uploaded(uploaded.filename):
    raise HTTPError(400, "File is not allowed")
  (_, suffix) = os.path.splitext(uploaded.filename.lower())
  tmp_directory = '/tmp/{0}'.format('uploaded')
  tmp_filename = '{0}{1}'.format(str(uuid.uuid4()), suffix)
  if not os.path.exists(tmp_directory):
    os.makedirs(tmp_directory)
  savepath = os.path.join(tmp_directory, tmp_filename)
  uploaded.save(savepath)
  return "File is saved successfully"

