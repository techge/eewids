#!/bin/sh

if [ $# -lt 1 ]; then
    echo
    echo "Usage: sudo ./start.sh [wifi-interface | --server]"
    echo
    echo "e.g. sudo ./start.sh wlan0    # for standalone version"
    echo "or   sudo ./start.sh --server # only start server without capturing"
    echo
    exit
fi

if [ "$EUID" -ne 0 ]
    then echo "Please run as root."
    exit
fi

# See if docker daemon is runnning and start otherwise
if [ \! -e "/var/run/docker.sock" ]
then
    echo "systemctl start docker"
    systemctl start docker
fi

# Instead of running the container as a specific user
# (see http://docs.grafana.org/installation/docker/#grafana-container-
#  using-bind-mounts)
# we will just change the owner rights to standard user id
if [ ! -d "data/grafana" ]; then
    mkdir -p data/grafana
    echo "Creating folder data/grafana and change owner rights for grafana:"
    echo "chown 472:472 data/grafana"
    chown 472:472 data/grafana
fi


if [ "$1" == "--server" ]
then

    docker-compose -f docker-compose.server.yml up -d
    echo
    echo "######################################################################"
    echo You can now connect/start the capture tool on your source.
    echo For more information have a look at
    echo https://github.com/techge/eewids/blob/master/doc/getting-started.md
    echo
    echo Afterwards, connect to http://localhost:3000 and login with admin:admin
    echo
    echo Press Enter to end Eewids
    echo
    echo "######################################################################"
    read

    echo "Killing everything now :)"
    echo
    docker-compose -f docker-compose.server.yml down

else

    export WIFI_DEVICE=$1
    docker-compose up -d
    echo
    echo "######################################################################"
    echo
    echo Connect to http://localhost:3000 and login with admin:admin
    echo
    echo Press Enter to end Eewids
    echo
    echo "######################################################################"

    read

    echo "Killing everything now :)"
    echo
    docker-compose down

    echo "Trying to restore WiFi to previous state (partly based on NetworkManager)"
    ifconfig ${WIFI_DEVICE}mon down
    iw dev ${WIFI_DEVICE}mon del
    nmcli device set $WIFI_DEVICE managed true

fi
