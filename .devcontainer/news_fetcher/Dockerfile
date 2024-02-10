FROM python:3.9.1-alpine3.12

RUN apk update && apk upgrade
RUN apk add --update --no-cache g++ gcc libxslt-dev logrotate tzdata
RUN cp /usr/share/zoneinfo/America/New_York /etc/localtime
RUN echo "America/New_York" >  /etc/timezone
RUN apk del tzdata

RUN pip3 install progress
RUN pip3 install daemons
RUN pip3 install filelock

RUN rm -rf /var/cache/apk/*
