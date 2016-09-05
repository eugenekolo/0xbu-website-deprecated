#!/bin/bash
###############################
#   000      BBBB  U   U
#  0  /0     B   B U   U
#  0 / 0 x x BBBB  U   U
#  0/  0  x  B   B U   U
#   000  x x BBBB   UUU
###############################
# Deploy the 0xBU Website!

# build the website container
sudo docker build -t 0xbu-website .

# run the website
sudo docker run -dt -v $PWD/ghost/content:/home/ghost/0xbu-website/ghost-app/content \
		    -v $PWD/certs:/etc/letsencrypt/live/0xbu.com \
		    -p 80:80 -p 443:443 -p 8000:8000 \
		    0xbu-website

# auto renew the certs every 90 days
# TODO
# certbot-auto

# do a bi-weekly backup of the website
# TODO

# do a weekly test of the website
# TODO

