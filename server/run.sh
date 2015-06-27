#!/bin/bash

docker run -d --name server -p 80:8080 \
  -v /var/log/server:/var/log \
  -v /etc/localtime:/etc/localtime:ro \
  a-hisame/server:1.0

