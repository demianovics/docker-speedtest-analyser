FROM node:lts-alpine AS build

# greet me :)
MAINTAINER Tobias Rös - <roes@amicaldo.de>

# install dependencies
RUN apk update && apk add \
  bash \
  git \
  nginx \
  nginx-mod-http-lua \
  python3 \
  py-pip


RUN pip install speedtest-cli

# remove default content
RUN rm -R /var/www/*

# create directory structure
RUN mkdir -p /etc/nginx
RUN mkdir -p /run/nginx
RUN mkdir -p /etc/nginx/global
RUN mkdir -p /var/www/html

# touch required files
RUN touch /var/log/nginx/access.log && touch /var/log/nginx/error.log

# install vhost config
ADD ./config/vhost.conf /etc/nginx/conf.d/default.conf
ADD config/nginxEnv.conf /etc/nginx/modules/nginxEnv.conf

# install webroot files
ADD ./ /var/www/html/

# install bower dependencies
RUN cd /var/www/html/ && yarn install

EXPOSE 80
EXPOSE 443

RUN chown -R nginx:nginx /var/www/html/
RUN chmod +x /var/www/html/config/run.sh
RUN chmod 755 /var/www/html/scripts/speedtestRunner.py
ENTRYPOINT ["/var/www/html/config/run.sh"]