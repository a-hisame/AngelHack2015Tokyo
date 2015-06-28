# Dockerfile
FROM ubuntu
MAINTAINER a-hisame <a.hisame@gmail.com>
RUN apt-get -y update
RUN apt-get -y install python python-pip
RUN pip install boto bottle
RUN apt-get -y install imagemagick
RUN mkdir -p /opt/a-hisame/server && mkdir -p /var/log/server
COPY . /opt/a-hisame/server

CMD python /opt/a-hisame/server/main.py >> /var/log/server/server.log 2>&1



