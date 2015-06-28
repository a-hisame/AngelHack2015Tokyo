#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import uuid
import json
import subprocess

import bottle
from bottle import route, run, view, static_file, template
from bottle import get, post, request, response
from bottle import HTTPError

import dao.dynamodb as dynamodb
import dao.s3 as s3

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


def _save_images():
  # validate uploaded thing
  uploaded = request.files.get('upload')
  if not _validate_uploaded(uploaded.filename):
    raise HTTPError(400, "File is not allowed")
  # save to local
  (_, suffix) = os.path.splitext(uploaded.filename.lower())
  tmp_directory = '/tmp/{0}'.format('uploaded')
  tmp_filename = '{0}'.format(str(uuid.uuid4()))
  if not os.path.exists(tmp_directory):
    os.makedirs(tmp_directory)
  savepath = '{0}{1}'.format(os.path.join(tmp_directory, tmp_filename), suffix)
  uploaded.save(savepath)
  # convert thumb
  thumb_file = 'thumb-{0}.jpg'.format(tmp_filename)
  thumb_path = os.path.join(tmp_directory, thumb_file)
  cmds = ['convert', '-resize', '320x', savepath, thumb_path] 
  subprocess.call(cmds)
  # upload to s3
  s3bucket = dynamodb.get_env('IMAGE_S3_BUCKET') 
  s3path = 'images/{0}'.format(thumb_file)
  s3.upload(thumb_path, s3bucket, s3path)
  return s3path 


@post('/{0}/api/upload'.format(__CONTEXT_ROOT))
def upload_image():
 req = dict(request.forms.decode())
 if req.get('name') in ['', None]:
   raise HTTPError(400, "name is required")
 s3path = _save_images()
 restaurant = req.get('location', req.get('restaurant', ''))
 print req, restaurant, s3path
 dynamodb.put_dish(req['name'], req.get('description', ''), restaurant, req.get('tags', ''), s3path)
 return "File is saved successfully"

