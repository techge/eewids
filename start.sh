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

# start via docker-compose.yml file
docker-compose up -d

if [ "$1" == "--server" ]
then

    echo
    echo "######################################################################"
    echo You could now connect/start the capture tool on your source.
    echo For more information have a look at
    echo https://github.com/techge/eewids/blob/master/doc/getting-started.md
    echo
    echo Afterwards, connect to http://localhost:3000 and login with admin:admin
    echo "######################################################################"
    echo
    echo Press Ctrl-c to end Eewids
    echo
    read

    echo "killing everything now :)"
    echo
    docker-compose down

else

    echo
    echo "######################################################################"
    echo
    echo Connect to http://localhost:3000 and login with admin:admin
    echo
    echo Press Enter to end Eewids
    echo
    echo "######################################################################"

    iw dev $1 interface add ${1}mon type monitor
    ifconfig ${1}mon up
    ID=$(docker run -d -ti --net=host --privileged --restart always eewids-cap ${1}mon)
    read

    echo "Killing everything now :)"
    echo
    docker kill $ID
    docker-compose down

    echo "Trying to restore WiFi to previous state (partly based on NetworkManager)"
    ifconfig ${1}mon down
    iw dev ${1}mon del
    nmcli device set $1 managed true

fi
