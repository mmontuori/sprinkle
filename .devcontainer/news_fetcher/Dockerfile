FROM mmontuori/pythonenv:latest

RUN apt update
RUN apt install -y  g++ gcc libxslt1-dev logrotate

RUN pip3 install progress
RUN pip3 install daemons
RUN pip3 install filelock

RUN rm -rf /var/cache/apk/*
