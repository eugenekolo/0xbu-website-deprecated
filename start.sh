#!/bin/bash
# This script is meant to be run inside a provision system by Docker
# i.e. after you've ran `docker build`.

set -e
BU_ROOT=/home/ghost/0xbu-website
GHOST_ROOT=$BU_ROOT/ghost-app

if [[ "$*" == npm*start* ]]; then
	# start nginx
	service nginx start

	# start ghost
	chown -R ghost:ghost $BU_ROOT
	su -c "cd $GHOST_ROOT && npm start --production &" ghost

	# start backend
	su -c "cd $BU_ROOT && python ./apps/app.py > app.py.log &" ghost
fi

bash -i
