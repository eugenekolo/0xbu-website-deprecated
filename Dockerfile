FROM node:4
MAINTAINER eugene@kolobyte.com
ENV BU_WEBSITE 1.0
ENV BU_ROOT /home/ghost/0xbu-website
ENV GHOST_ROOT $BU_ROOT/ghost-app

# initialize
RUN apt-get update && \
apt-get install -y zip && \
apt-get install -y unzip && \
apt-get install -y git && \
apt-get install -y wget && \
apt-get install -y python-dev && \
apt-get install -y python-pip

RUN groupadd ghost && \
useradd --create-home --home-dir /home/ghost -g ghost ghost
USER ghost
RUN mkdir $BU_ROOT

# install ghost
RUN mkdir $GHOST_ROOT && \
cd $GHOST_ROOT && \
wget https://ghost.org/zip/ghost-latest.zip && \
unzip ghost-latest.zip && \
npm install --production

COPY conf/config.js $GHOST_ROOT/config.js

# install nginx + letsencrypt
USER root
RUN apt-get install -y nginx

# install backend
RUN pip install flask
RUN pip install flask-cors

# transfer over backend
COPY apps $BU_ROOT/apps

# transfer over configs
COPY conf $BU_ROOT/conf
COPY conf/nginx.conf /etc/nginx/nginx.conf

# transfer over keys
COPY certs/privkey.pem /etc/letsencrypt/live/0xbu.com/privkey.pem
COPY certs/fullchain.pem /etc/letsencrypt/live/0xbu.com/fullchain.pem
VOLUME /etc/letsencrypt/live/0xbu.com

# transfer over content
COPY ghost/content $GHOST_ROOT/content
VOLUME $GHOST_ROOT/content

# start nginx + ghost + backend
COPY start.sh $BU_ROOT
EXPOSE 443
EXPOSE 80
RUN chown -R ghost:ghost $BU_ROOT
ENTRYPOINT ["/home/ghost/0xbu-website/start.sh"]
CMD ["npm", "start"]
