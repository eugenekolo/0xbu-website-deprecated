#!/bin/bash
#
# This script is ran in docker container on 'docker run <container>'
#
# If this script is called as `./provision start`, then it will start nginx and ghost`
# otherwise, the script just gives the caller a debug shell
#

set -e
BU_ROOT="/website"
GHOST_ROOT="$BU_ROOT/ghost"

if [[ "$*" == *start* ]]; then
    # Start nginx
    service nginx start

    # Start ghost
    su -c "cd $GHOST_ROOT && npm start --production &" ghost
fi

bash -i

