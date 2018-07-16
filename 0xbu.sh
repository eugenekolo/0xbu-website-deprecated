#!/bin/bash
# Deploy the 0xBU Website!

IMAGE_NAME="0xbu-website-image"
CONTAINER_NAME="0xbu-website-container"

BACKUP_FREQ="1209600"
PING_FREQ="86400"
CERT_FREQ="86400"

function start()
{
    echo '###############################'
    echo '#   000        BBBB   U   U    '
    echo '#  0  /0       B   B  U   U    '
    echo '#  0 / 0  x x  BBBB   U   U    '
    echo '#  0/  0   x   B   B  U   U    '
    echo '#   000   x x  BBBB    UUU     '
    echo '###############################'
    echo '[*] Configuration: '
    echo "[+] IMAGE_NAME=$IMAGE_NAME"
    echo "[+] CONTAINER_NAME=$CONTAINER_NAME"
    echo "[+] BACKUP_FREQ=$BACKUP_FREQ"
    echo "[+] PING_FREQ=$PING_FREQ"
    echo "[+] CERT_FREQ=$CERT_FREQ"
    echo ""
    echo '[*] Launching 0xBU website...'

    # build the website image
    if [[ "$(sudo docker images -q $IMAGE_NAME 2> /dev/null)" == "" ]]; then
        echo '[+] Building website image'
        sudo docker build -t $IMAGE_NAME .
    else
        echo '[+] Website image already built'
    fi

    # run the website
    if [[ ! "$(sudo docker ps -a --filter='name=$CONTAINER_NAME' | grep '$CONTAINER_NAME')" ]]; then
        echo '[+] Starting new website docker container'
        sudo docker run -dt --name $CONTAINER_NAME \
                    -v $PWD/ghost/content:/website/ghost/content \
                    -p 80:80 \
                    $IMAGE_NAME
    else
        echo '[+] Container already exists, starting it'
        sudo docker start $CONTAINER_NAME
    fi

    # Give it some time to launch
    sleep 8

    # do backup of the website
    if [[ ! "$(ps aux | grep -v grep | grep 'backup-data.sh')" ]]; then
        echo "[+] Launching "$BACK_FREQ"s backup of website via backup-data.sh"
        watch -t -n$BACKUP_FREQ ""$PWD"/scripts/backup-data.sh" &> /dev/null &
    else
        echo "[+] Backup script already running"
    fi

    # do test of the website
    if [[ ! "$(ps aux | grep -v grep | grep 'ping-website.sh')" ]]; then
        echo "[+] Launching "$PING_FREQ"s ping of website via ping-website.sh"
        watch -t -n$PING_FREQ ""$PWD"/scripts/ping-website.sh" &> /dev/null &
    else
        echo "[+] Ping script already running"
    fi

    echo "[*] 0xBU website launched."
}

function stop()
{
    echo "[*] Stopping website"

    if [[ "$(sudo docker ps -a --filter='name=$CONTAINER_NAME' | grep '$CONTAINER_NAME')" ]]; then
        echo "[+] Stopping container $CONTAINER_NAME"
        sudo docker stop $CONTAINER_NAME
    fi

    if [[ $(ps aux | grep -v grep | grep 'backup-data.sh' | awk '{print $2}') ]]; then
        echo "[+] Killing backup data script"
        kill $(ps aux | grep -v grep | grep 'backup-data.sh' | awk '{print $2}')
    fi

    if [[ $(ps aux | grep -v grep | grep 'ping-website.sh' | awk '{print $2}') ]]; then
        echo "[+] Killing ping website script"
        kill $(ps aux | grep -v grep | grep 'ping-website.sh' | awk '{print $2}')
    fi

    echo "[*] Stopped website"
}

function destroy()
{
    stop
    echo "[*] Destroying website"

    if [[ "$(sudo docker ps -a --filter='name=$CONTAINER_NAME' | grep '$CONTAINER_NAME')" ]]; then
        echo "[+] Removing container $CONTAINER_NAME"
        sudo docker rm "$CONTAINER_NAME"
    fi

    if [[ "$(sudo docker images -q $IMAGE_NAME)" ]]; then
        echo "[+] Removing image $IMAGE_NAME"
        sudo docker rmi "$IMAGE_NAME"
    fi

    echo "[*] Destroyed website"
}

function debug()
{
    sudo docker exec -it "$CONTAINER_NAME" /bin/sh
}

function help()
{
    echo "Invalid command. Supported commands: [start|stop|destroy|debug]"
}



ACTION=$1

case "$ACTION" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    destroy)
        destroy
        ;;
    debug)
        debug
        ;;
    *)
        help
        ;;
esac

