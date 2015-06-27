#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

from bottle import run

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import controller.static
import controller.index


if __name__ == '__main__':
  run(host='0.0.0.0', port=8080)

